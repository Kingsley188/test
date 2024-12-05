import os  
import shutil  
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

class DrawingSorterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("图纸自动归类工具")
        self.root.geometry("600x400")
        
        # 创建主框架
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 路径选择部分
        self.path_frame = ttk.LabelFrame(self.main_frame, text="选择文件夹", padding="5")
        self.path_frame.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        self.path_var = tk.StringVar()
        self.path_entry = ttk.Entry(self.path_frame, textvariable=self.path_var, width=50)
        self.path_entry.grid(row=0, column=0, padx=5)
        
        self.browse_button = ttk.Button(self.path_frame, text="浏览", command=self.browse_folder)
        self.browse_button.grid(row=0, column=1, padx=5)
        
        # 开始按钮
        self.start_button = ttk.Button(self.main_frame, text="开始归类", command=self.start_sorting)
        self.start_button.grid(row=1, column=0, columnspan=3, pady=10)
        
        # 进度显示区域
        self.log_frame = ttk.LabelFrame(self.main_frame, text="处理日志", padding="5")
        self.log_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        self.log_text = tk.Text(self.log_frame, height=15, width=60)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 添加滚动条
        self.scrollbar = ttk.Scrollbar(self.log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.log_text['yscrollcommand'] = self.scrollbar.set
        
    def browse_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.path_var.set(folder_path)
            
    def log_message(self, message):
        self.log_text.insert(tk.END, message + '\n')
        self.log_text.see(tk.END)
        self.root.update()
            
    def start_sorting(self):
        source_path = self.path_var.get().strip()
        if not source_path:
            messagebox.showerror("错误", "请选择要整理的文件夹！")
            return
            
        if not os.path.exists(source_path):
            messagebox.showerror("错误", f"路径 '{source_path}' 不存在！")
            return
            
        self.log_text.delete(1.0, tk.END)
        self.sort_drawings(source_path)
        
    def sort_drawings(self, source_path):
        # 定义目标文件夹列表  
        target_folders = ['A0', 'A1', 'A2', 'A3', 'A4']  
        
        # 确保每个目标文件夹都存在  
        for folder in target_folders:  
            folder_path = os.path.join(source_path, folder)
            if not os.path.exists(folder_path):  
                os.makedirs(folder_path)
                self.log_message(f"创建文件夹: {folder}")
        
        # 遍历指定目录下的所有文件和文件夹  
        for item in os.listdir(source_path):  
            item_path = os.path.join(source_path, item)
            if os.path.isdir(item_path):  
                continue  
        
            target_folder = None  
        
            # 检查文件名，确定目标文件夹  
            for prefix in ['_A0', '_A0+', '_A1', '_A2', '_A3', '_A4']:  
                if prefix in item:  
                    target_folder = prefix[1:].rstrip('+')  
                    break  
        
            # 如果找到了目标文件夹，则移动文件  
            if target_folder:  
                target_path = os.path.join(source_path, target_folder, item)  
                try:  
                    shutil.move(item_path, target_path)  
                    self.log_message(f"已移动: {item} -> {target_folder}")
                except shutil.Error as e:  
                    self.log_message(f"错误: 移动 {item} 时出错 - {str(e)}")
        
        self.log_message("\n文件归类完成！")
        messagebox.showinfo("完成", "文件归类已完成！")

def main():
    root = tk.Tk()
    app = DrawingSorterGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
