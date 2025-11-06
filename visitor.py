import requests
import time
import sys
from datetime import datetime
import os

# 屏蔽 SSL 警告
import warnings
warnings.filterwarnings('ignore', message='Unverified HTTPS request')

def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def load_targets_from_file(file_name="ip.txt"):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, file_name)
    
    if not os.path.exists(file_path):
        file_path = os.path.join(os.getcwd(), file_name)
        if not os.path.exists(file_path):
            with open("error.log", "a", encoding="utf-8") as f:
                f.write("[{}] 未找到 {} 文件\n".format(get_current_time(), file_name))
            sys.exit(1)
    
    if not os.access(file_path, os.R_OK):
        with open("error.log", "a", encoding="utf-8") as f:
            f.write("[{}] 无权限读取 {}\n".format(get_current_time(), file_path))
            sys.exit(1)
    
    targets = set()
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            target = line.strip()
            if target and not target.startswith("#"):
                if not target.startswith(("http://", "https://")):
                    target = f"https://{target}"
                targets.add(target)
    
    targets = list(targets)
    if not targets:
        with open("error.log", "a", encoding="utf-8") as f:
            f.write("[{}] {} 无有效目标\n".format(get_current_time(), file_path))
        sys.exit(1)
    
    # 用 format 语法，彻底避免 f-string 错误
    with open("网页.log", "a", encoding="utf-8") as f:
        f.write("[{}] 成功加载 {} 个目标\n".format(get_current_time(), len(targets)))
    return targets

def infinite_visit_batch(targets, interval=5):
    log_cache = []
    cache_threshold = 3
    session = requests.Session()
    
    while True:
        for target in targets:
            try:
                response = session.get(
                    target, 
                    timeout=8,
                    verify=False,
                    headers={'User-Agent': 'Mozilla/5.0 (Linux; Android) AppleWebKit/537.36'},
                    stream=False,
                    allow_redirects=True
                )
                log_msg = "[{}] 成功 | {} | 状态码：{}\n".format(get_current_time(), target, response.status_code)
            except requests.exceptions.ConnectionError:
                log_msg = "[{}] 失败 | {} | 状态码：-1\n".format(get_current_time(), target)
            except requests.exceptions.Timeout:
                log_msg = "[{}] 失败 | {} | 状态码：-2\n".format(get_current_time(), target)
            except Exception:
                log_msg = "[{}] 失败 | {} | 状态码：-999\n".format(get_current_time(), target)
            
            log_cache.append(log_msg)
            if len(log_cache) >= cache_threshold:
                with open("网页.log", "a", encoding="utf-8") as f:
                    f.write(''.join(log_cache))
                log_cache.clear()
        
        time.sleep(interval)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        # 彻底放弃 f-string，全用 format 避免语法错误
        with open("error.log", "a", encoding="utf-8") as f:
            f.write("[{}] 用法错误：python3 visitor.py ip.txt [间隔(≥5秒)]\n".format(get_current_time()))
        sys.exit(1)
    
    arg1 = sys.argv[1]
    visit_interval = int(sys.argv[2]) if (len(sys.argv) >=3 and sys.argv[2].isdigit() and int(sys.argv[2])>=5) else 5
    
    if arg1.lower() == "ip.txt" or os.path.isfile(arg1):
        targets = load_targets_from_file(arg1)
    else:
        target = arg1.strip()
        if not target.startswith(("http://", "https://")):
            target = f"https://{target}"
        targets = [target]
        with open("网页.log", "a", encoding="utf-8") as f:
            f.write("[{}] 单个目标：{}\n".format(get_current_time(), target))
    
    try:
        infinite_visit_batch(targets, visit_interval)
    except KeyboardInterrupt:
        with open("网页.log", "a", encoding="utf-8") as f:
            f.write("[{}] 程序已停止\n".format(get_current_time()))
        sys.exit(0)
    except Exception as e:
        with open("error.log", "a", encoding="utf-8") as f:
            f.write("[{}] 启动失败：{}\n".format(get_current_time(), str(e)))
        sys.exit(1)