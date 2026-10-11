import os
import sys
import subprocess
import asyncio
def update_version():
    try:
        subprocess.run(["git","fetch"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        result = subprocess.run(
            ["git", "rev-list", "HEAD..origin/main"], # Thay "main" bằng tên nhánh của bạn nếu dùng nhánh khác
            capture_output=True, 
            text=True, 
            check=True
        )
        print(result)
        commits_behind = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
        if commits_behind > 0:
            print(f" Phát hiện {commits_behind} commit mới trên GitHub. Tiến hành cập nhật...")
            
            # 3. Kéo toàn bộ code mới về (Git Pull)
            subprocess.run(["git", "pull"], check=True)
            print(" Đã tải xong toàn bộ mã nguồn mới.")
            # Tại động cài đặt các thư viện nếu có
            if os.path.exists("requirements.txt"):
                print("Đang kiểm tra và cập nhật các thư viện (pip)...")
                subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
            asyncio.sleep(2)
            print("Hoàn tất các cập nhật thư viện")
            # Lấy đừng dẫn của chính nó là khởi động lại
            current_script = os.path.abspath(sys.argv[0])
            #Tạo tiến trình đọc lập để chạy
            subprocess.Popen([sys.executable, current_script] + sys.argv[1:])
            #Thoát khỏi phiên bản cũ
            sys.exit(0)
        else:
            print("Bạn đang sử dụng phiên bản mới nhất.")
    except subprocess.CalledProcessError as e:
        print(f"Lỗi lệnh Git: {e}")
    except Exception as e:
        print(f"Lỗi không xác định: {e}")

if __name__ =="__main__":
    update_version()