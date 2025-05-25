import os
import sqlite3
from pathlib import Path
import re
from urllib.parse import unquote
import multiprocessing
from concurrent.futures import ProcessPoolExecutor
import time
from typing import List, Dict, Any
import queue
import threading

# 配置
MEDIA_DIR = r"D:\cbeifenn\Downloads\TikTokDownloader_V5.4_WIN\标签\大姐姐"
# MEDIA_DIR = r"D:\cbeifenn\Downloads\TikTokDownloader_V5.4_WIN"
# MEDIA_DIR = "/Users/bu/Downloads/picpro"
DB_PATH = "album.db"
BATCH_SIZE = 1000  # 批量处理的大小
MAX_WORKERS = max(1, multiprocessing.cpu_count() // 2)  # 使用CPU核心数的一半，至少为1

# 支持的媒体格式
SUPPORTED_IMAGE_FORMATS = [
    '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp',
    '.heic', '.heif'
]

SUPPORTED_VIDEO_FORMATS = [
    '.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm', '.mkv', '.m4v', '.ts'
]

# 正则表达式，用于解析标签
re_param = re.compile(r'([^:]+):\s*("(?:\\.|[^\\"])+"|[^,]*)(?:,|$)')
re_imagesize = re.compile(r"^(\d+)x(\d+)$")

def initialize_database():
    """初始化数据库表结构"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # 初始化表结构
    cur.executescript("""
    DROP TABLE IF EXISTS media_tag;
    DROP TABLE IF EXISTS tag;
    DROP TABLE IF EXISTS media;

    CREATE TABLE media (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT,
        filepath TEXT,
        media_type TEXT,
        size INTEGER DEFAULT NULL,
        created_at TEXT,
        modified_at TEXT
    );

    CREATE TABLE tag (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE
    );

    CREATE TABLE media_tag (
        media_id INTEGER,
        tag_id INTEGER,
        PRIMARY KEY (media_id, tag_id),
        FOREIGN KEY (media_id) REFERENCES media(id) ON DELETE CASCADE,
        FOREIGN KEY (tag_id) REFERENCES tag(id) ON DELETE CASCADE
    );
    """)

    # 创建点赞和收藏记录表
    cur.execute("""
    CREATE TABLE media_favorite (
        filepath TEXT PRIMARY KEY,
        filename TEXT NOT NULL,
        is_liked BOOLEAN DEFAULT 0,
        is_favorited BOOLEAN DEFAULT 0,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (filepath) REFERENCES media(filepath) ON DELETE CASCADE
    );
    """)

    # 创建索引
    # media表索引
    cur.execute("CREATE INDEX IF NOT EXISTS idx_media_filename ON media(filename);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_media_filepath ON media(filepath);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_media_type ON media(media_type);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_media_created_at ON media(created_at);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_media_modified_at ON media(modified_at);")

    # tag表索引
    cur.execute("CREATE INDEX IF NOT EXISTS idx_tag_name ON tag(name);")

    # media_tag表索引
    cur.execute("CREATE INDEX IF NOT EXISTS idx_media_tag_media_id ON media_tag(media_id);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_media_tag_tag_id ON media_tag(tag_id);")

    # media_favorite表索引
    cur.execute("CREATE INDEX IF NOT EXISTS idx_media_favorite_filename ON media_favorite(filename);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_media_favorite_is_liked ON media_favorite(is_liked);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_media_favorite_is_favorited ON media_favorite(is_favorited);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_media_favorite_updated_at ON media_favorite(updated_at);")

    conn.commit()
    conn.close()
    print("✅ 数据库表结构初始化完成")

def parse_tags_from_file(txt_path):
    """从文本文件中解析标签"""
    try:
        with open(txt_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            return parse_generation_parameters(content)
    except Exception as e:
        print(f"无法解析标签文件 {txt_path}: {e}")
        return {"pos_prompt": []}

def parse_generation_parameters(x: str):
    """解析生成参数，提取标签"""
    res = {}
    prompt = ""
    negative_prompt = ""
    done_with_prompt = False
    if not x:
        return {"meta": {}, "pos_prompt": [], "lora": [], "lyco": []}
    
    # 分割文本内容
    lines = x.strip().split("\n")
    lastline = lines[-1] if lines else ""
    lines = lines[:-1] if lines else []
    
    # 检查最后一行是否包含参数
    if len(re_param.findall(lastline)) < 3:
        lines.append(lastline)
        lastline = ""
    
    # 处理特殊情况
    if len(lines) == 1 and lines[0].startswith("Postprocess"):
        lastline = lines[0]
        lines = []
    
    # 提取提示词
    for i, line in enumerate(lines):
        line = line.strip()
        if line.startswith("Negative prompt:"):
            done_with_prompt = True
            line = line[16:].strip()

        if done_with_prompt:
            negative_prompt += ("" if negative_prompt == "" else "\n") + line
        else:
            prompt += ("" if prompt == "" else "\n") + line
    
    # 解析参数
    for k, v in re_param.findall(lastline):
        try:
            if len(v) == 0:
                res[k] = v
                continue
            if v[0] == '"' and v[-1] == '"':
                v = unquote(v)

            m = re_imagesize.match(v)
            if m is not None:
                res[f"{k}-1"] = m.group(1)
                res[f"{k}-2"] = m.group(2)
            else:
                res[k] = v
        except Exception:
            print(f"Error parsing \"{k}: {v}\"")
    
    # 简化提取标签
    tags = []
    if prompt:
        # 按逗号分割提示词，提取标签
        for tag in prompt.split(","):
            tag = tag.strip()
            if tag:
                tags.append(tag)
    
    return {"pos_prompt": tags}

def process_file_batch(file_batch: List[Path]) -> List[Dict[str, Any]]:
    """处理一批文件"""
    results = []
    for path in file_batch:
        if not path.is_file():
            continue
            
        suffix = path.suffix.lower()
        if suffix in SUPPORTED_IMAGE_FORMATS + SUPPORTED_VIDEO_FORMATS:
            media_type = "image" if suffix in SUPPORTED_IMAGE_FORMATS else "video"
            stat = path.stat()
            file_size = stat.st_size if media_type == "video" else None
            
            # 处理标签
            tags = []
            txt_path = path.with_suffix('.txt')
            if txt_path.exists():
                parsed_data = parse_tags_from_file(txt_path)
                tags = parsed_data.get("pos_prompt", [])
            
            results.append({
                'filename': path.name,
                'filepath': str(path.resolve()),
                'media_type': media_type,
                'size': file_size,
                'created_at': int(stat.st_ctime),
                'modified_at': int(stat.st_mtime),
                'tags': tags
            })
    
    return results

def save_to_database(results: List[Dict[str, Any]], db_path: str):
    """将处理结果保存到数据库"""
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    try:
        # 开始事务
        cur.execute("BEGIN TRANSACTION")
        
        # 批量插入媒体文件
        media_data = [(
            r['filename'],
            r['filepath'],
            r['media_type'],
            r['size'],
            r['created_at'],
            r['modified_at']
        ) for r in results]
        
        cur.executemany("""
            INSERT OR IGNORE INTO media 
            (filename, filepath, media_type, size, created_at, modified_at)
            VALUES (?, ?, ?, ?, datetime(?,'unixepoch'), datetime(?,'unixepoch'))
        """, media_data)
        
        # 获取插入的媒体ID
        for result in results:
            cur.execute("SELECT id FROM media WHERE filepath = ?", (result['filepath'],))
            media_id = cur.fetchone()[0]
            
            # 处理标签
            for tag_name in result['tags']:
                # 获取或创建标签
                cur.execute("SELECT id FROM tag WHERE name = ?", (tag_name,))
                tag_result = cur.fetchone()
                if tag_result:
                    tag_id = tag_result[0]
                else:
                    cur.execute("INSERT INTO tag (name) VALUES (?)", (tag_name,))
                    tag_id = cur.lastrowid
                
                # 关联媒体和标签
                cur.execute("""
                    INSERT OR IGNORE INTO media_tag (media_id, tag_id)
                    VALUES (?, ?)
                """, (media_id, tag_id))
        
        # 提交事务
        conn.commit()
        
    except Exception as e:
        print(f"保存到数据库时出错: {e}")
        conn.rollback()
    finally:
        conn.close()

def process_media_files():
    """并行处理媒体文件"""
    # 获取所有文件路径
    all_files = list(Path(MEDIA_DIR).rglob("*"))
    total_files = len(all_files)
    print(f"找到 {total_files} 个文件")
    
    # 将文件分批
    batches = [all_files[i:i + BATCH_SIZE] for i in range(0, len(all_files), BATCH_SIZE)]
    total_batches = len(batches)
    print(f"分成 {total_batches} 批处理")
    
    # 创建进度队列
    progress_queue = queue.Queue()
    
    def progress_monitor():
        processed = 0
        while processed < total_batches:
            try:
                batch_num = progress_queue.get(timeout=1)
                processed += 1
                print(f"进度: {processed}/{total_batches} 批 ({processed/total_batches*100:.1f}%)")
            except queue.Empty:
                continue
    
    # 启动进度监控线程
    monitor_thread = threading.Thread(target=progress_monitor)
    monitor_thread.start()
    
    # 使用进程池并行处理
    with ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = []
        for i, batch in enumerate(batches):
            future = executor.submit(process_file_batch, batch)
            future.add_done_callback(lambda f, i=i: progress_queue.put(i))
            futures.append(future)
        
        # 收集所有结果
        all_results = []
        for future in futures:
            all_results.extend(future.result())
    
    # 等待进度监控线程结束
    monitor_thread.join()
    
    # 批量保存到数据库
    print("正在保存到数据库...")
    save_to_database(all_results, DB_PATH)
    print("✅ 媒体文件处理完成")

def main():
    """主函数"""
    start_time = time.time()
    
    # 初始化数据库
    initialize_database()
    
    # 处理媒体文件
    process_media_files()
    
    end_time = time.time()
    print(f"✅ 全部任务完成，耗时: {end_time - start_time:.1f} 秒")

if __name__ == "__main__":
    main() 