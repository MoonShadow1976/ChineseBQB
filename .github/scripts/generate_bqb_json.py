import os
import json
import sys

def generate_json_data(repo_owner, repo_name, branch):
    base_url = f"https://raw.githubusercontent.com/{repo_owner}/{repo_name}/{branch}"
    
    # 初始化数据结构
    data = {
        "status": 1000,
        "info": "ChineseBQB的Github数据源",
        "data": []
    }
    
    # 排除的目录（不需要处理的文件夹）
    excluded_dirs = ['.github', '.git', '__pycache__', '.vscode', 'scripts']
    
    # 遍历仓库中的所有目录
    for root, dirs, files in os.walk('.'):
        # 跳过隐藏目录和排除的目录
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in excluded_dirs]
        
        # 获取当前目录的相对路径
        rel_path = os.path.relpath(root, '.')
        
        # 跳过根目录
        if rel_path == '.':
            continue
            
        # 处理当前目录中的文件
        for file in files:
            # 跳过隐藏文件和非图像文件（根据需要调整扩展名）
            if not file.startswith('.') and file.lower().endswith(('.gif', '.jpg', '.jpeg', '.png', '.webp')):
                # 构建文件条目
                entry = {
                    "name": file,
                    "category": os.path.basename(rel_path),
                    "url": f"{base_url}/{rel_path}/{file}"
                }
                data["data"].append(entry)
    
    return data

if __name__ == "__main__":
    # 从环境变量获取仓库信息
    repo_owner = os.environ.get('GITHUB_REPOSITORY_OWNER', 'zhaoolee')
    repo_name = os.environ.get('GITHUB_REPOSITORY').split('/')[-1] if os.environ.get('GITHUB_REPOSITORY') else 'ChineseBQB'
    branch = os.environ.get('GITHUB_REF_NAME', 'master')
    
    # 生成JSON数据
    json_data = generate_json_data(repo_owner, repo_name, branch)
    
    # 写入文件
    with open('wutheringwaves_bqb.json', 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)
    
    print("JSON文件已生成")