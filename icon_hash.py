import warnings
import requests
import base64
import mmh3
import argparse
import os
import urllib3

warnings.simplefilter('ignore', urllib3.exceptions.InsecureRequestWarning)

def print_ascii_art():
    ascii_art = r'''
██╗ ██████╗ ██████╗ ███╗   ██╗        ██╗  ██╗ █████╗ ███████╗██╗  ██╗
██║██╔════╝██╔═══██╗████╗  ██║        ██║  ██║██╔══██╗██╔════╝██║  ██║
██║██║     ██║   ██║██╔██╗ ██║        ███████║███████║███████╗███████║
██║██║     ██║   ██║██║╚██╗██║        ██╔══██║██╔══██║╚════██║██╔══██║
██║╚██████╗╚██████╔╝██║ ╚████║███████╗██║  ██║██║  ██║███████║██║  ██║
╚═╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
                                                                 1.0
                                                     Trendy_man@小小怪
    '''
    print(ascii_art)

def get_icon_hash(url):
    try:
        resp = requests.get(url, verify=False)
        if resp.status_code != 200:
            print(f"无法访问 {url}，状态码: {resp.status_code}")
            return None

        favicon_data = resp.content
        b64_data = base64.encodebytes(favicon_data)
        icon_hash_value = mmh3.hash(b64_data)
        return icon_hash_value
    except requests.exceptions.RequestException as e:
        print(f"无法访问 {url}，错误信息: {e}")
        return None

def get_image_hash(image_path):
    print(f"正在处理路径: {image_path}")
    if os.path.isdir(image_path):
        print(f"路径 {image_path} 是一个目录，请提供文件路径。")
        return None

    try:
        with open(image_path, "rb") as f:
            image_data = f.read()
        b64_data = base64.encodebytes(image_data)
        image_hash = mmh3.hash(b64_data)
        return image_hash
    except FileNotFoundError:
        print(f"文件 {image_path} 未找到。")
        return None

def parse_args():
    parser = argparse.ArgumentParser(description='计算网站的 icon_hash 或图片的哈希值')
    parser.add_argument('-u', '--url', type=str, help='单个网站的 URL，例如 https://www.baidu.com', required=False)
    parser.add_argument('-r', '--readfile', type=str, help='读取文件中的 URL，每行一个 URL', required=False)
    # 使用 nargs='+' 来接收一个或多个图片文件路径
    parser.add_argument('-i', '--image', type=str, nargs='+', help='图片路径（可传多个），用于计算图片哈希', required=False)
    return parser.parse_args()

def main():
    print_ascii_art()
    args = parse_args()

    if args.url:
        icon_hash = get_icon_hash(args.url)
        if icon_hash is not None:
            print(f"icon_hash for {args.url}: {icon_hash}")

    elif args.readfile:
        try:
            with open(args.readfile, 'r') as file:
                paths = file.readlines()
                for path in paths:
                    path = path.strip()
                    # 简单判断是否是图片（可根据需要调整）
                    if path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                        image_hash = get_image_hash(path)
                        if image_hash is not None:
                            print(f"Image hash for {path}: {image_hash}")
                    else:
                        icon_hash = get_icon_hash(path)
                        if icon_hash is not None:
                            print(f"icon_hash for {path}: {icon_hash}")
        except FileNotFoundError:
            print(f"File {args.readfile} not found.")

    elif args.image:
        # 这里 args.image 是一个列表，无论用户输入一个还是多个文件，都可以统一处理
        for image_path in args.image:
            image_hash = get_image_hash(image_path)
            if image_hash is not None:
                print(f"Image hash for {image_path}: {image_hash}")

    else:
        print("请提供 URL (-u)、文件路径 (-r) 或图片路径 (-i)")

if __name__ == "__main__":
    main()