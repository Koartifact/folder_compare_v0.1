import os
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime

def compare_folders():
    dir_a = entry_a.get()
    dir_b = entry_b.get()

    if not dir_a or not dir_b:
        messagebox.showwarning("경고", "두 폴더를 모두 선택해주세요.")
        return

    try:
        # 두 폴더의 파일 목록 가져오기
        files_a = set(os.listdir(dir_a))
        files_b = set(os.listdir(dir_b))

        # A에만 있는 항목 추출
        global only_in_a # 저장 기능을 위해 전역 변수화
        only_in_a = sorted(list(files_a - files_b))

        # 결과창 업데이트
        result_list.delete(0, tk.END)
        if not only_in_a:
            result_list.insert(tk.END, "모든 파일이 일치합니다!")
            btn_save.config(state=tk.DISABLED)
        else:
            for item in only_in_a:
                result_list.insert(tk.END, item)
            btn_save.config(state=tk.NORMAL) # 결과가 있으면 저장 버튼 활성화
            
    except Exception as e:
        messagebox.showerror("오류", f"오류가 발생했습니다: {e}")

def save_to_txt():
    if not only_in_a:
        return
    
    # 저장할 파일 경로 선택
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt")],
        initialfile=f"비교결과_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    )
    
    if file_path:
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(f"기준 폴더: {entry_a.get()}\n")
                f.write(f"대상 폴더: {entry_b.get()}\n")
                f.write("-" * 50 + "\n")
                f.write(f"검색된 누락 항목 ({len(only_in_a)}개):\n")
                for item in only_in_a:
                    f.write(f"- {item}\n")
            messagebox.showinfo("성공", "결과가 텍스트 파일로 저장되었습니다.")
        except Exception as e:
            messagebox.showerror("오류", f"파일 저장 중 오류 발생: {e}")

def browse_folder(entry):
    folder = filedialog.askdirectory()
    if folder:
        entry.delete(0, tk.END)
        entry.insert(0, folder)

# --- GUI 설정 ---
root = tk.Tk()
root.title("폴더 비교 및 리포트 생성기")
root.geometry("500x550")

# 폴더 선택 영역
tk.Label(root, text="기준 폴더 (A):", font=("돋움", 10, "bold")).pack(pady=5)
frame_a = tk.Frame(root)
frame_a.pack()
entry_a = tk.Entry(frame_a, width=50)
entry_a.pack(side=tk.LEFT, padx=5)
tk.Button(frame_a, text="찾기", command=lambda: browse_folder(entry_a)).pack(side=tk.LEFT)

tk.Label(root, text="비교 대상 폴더 (B):", font=("돋움", 10, "bold")).pack(pady=5)
frame_b = tk.Frame(root)
frame_b.pack()
entry_b = tk.Entry(frame_b, width=50)
entry_b.pack(side=tk.LEFT, padx=5)
tk.Button(frame_b, text="찾기", command=lambda: browse_folder(entry_b)).pack(side=tk.LEFT)

# 작업 버튼
btn_compare = tk.Button(root, text="비교 시작", command=compare_folders, bg="#2196F3", fg="white", width=20, height=2)
btn_compare.pack(pady=15)

# 결과 표시
tk.Label(root, text="[결과 목록]").pack()
result_list = tk.Listbox(root, width=60, height=12)
result_list.pack(pady=5)

# 저장 버튼
btn_save = tk.Button(root, text="결과를 .txt로 저장", command=save_to_txt, bg="#4CAF50", fg="white", state=tk.DISABLED, width=20)
btn_save.pack(pady=10)

only_in_a = [] # 결과 담을 리스트 초기화
root.mainloop()