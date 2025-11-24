import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import csv
import os

FILE_NAME = "studentMarks.txt"

class StudentManagerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Student Manager")
        self.master.geometry("1000x600")
        self.master.configure(bg="#f6fbf6")

        self.students = []
        self.total_students_declared = 0

        self._setup_style()
        self._build_layout()

        self.load_file(FILE_NAME, silent=True)

    def _setup_style(self):
        style = ttk.Style(self.master)
        try:
            style.theme_use('clam')
        except Exception:
            pass
        style.configure('TFrame', background='#ffffff')
        style.configure('Header.TLabel', background='#f6fbf6', font=('Segoe UI', 18, 'bold'), foreground='#0b6b3a')
        style.configure('Nav.TButton', background='#0b6b3a', foreground='white', font=('Segoe UI', 10, 'bold'))
        style.map('Nav.TButton', background=[('active', '#0e8c4a')])
        style.configure('Treeview', font=('Segoe UI', 10), rowheight=26)
        style.configure('Treeview.Heading', font=('Segoe UI', 10, 'bold'))

    def _build_layout(self):
        # Header Label
        header_frame = ttk.Frame(self.master, padding=(10,10))
        header_frame.pack(fill='x')
        ttk.Label(header_frame, text='Student Records', style='Header.TLabel').pack(side='left')

        container = ttk.Frame(self.master)
        container.pack(fill='both', expand=True, padx=10, pady=10)

        nav = ttk.Frame(container, width=180)
        nav.pack(side='left', fill='y', padx=(0,10))

        # Buttons order
        ttk.Button(nav, text='View All', style='Nav.TButton', command=self.display_all).pack(fill='x', pady=6)
        ttk.Button(nav, text='Find Student', style='Nav.TButton', command=self.find_student_popup).pack(fill='x', pady=6)
        ttk.Button(nav, text='Add Student', style='Nav.TButton', command=self.add_student).pack(fill='x', pady=6)
        ttk.Button(nav, text='Update Student', style='Nav.TButton', command=self.update_student_popup).pack(fill='x', pady=6)
        ttk.Button(nav, text='Delete Student', style='Nav.TButton', command=self.delete_student_popup).pack(fill='x', pady=6)
        ttk.Button(nav, text='Highest Score', style='Nav.TButton', command=self.highest_score).pack(fill='x', pady=6)
        ttk.Button(nav, text='Lowest Score', style='Nav.TButton', command=self.lowest_score).pack(fill='x', pady=6)
        ttk.Button(nav, text='Filter by Grade', style='Nav.TButton', command=self._filter_by_grade_popup).pack(fill='x', pady=6)
        ttk.Button(nav, text='Sort Records', style='Nav.TButton', command=self.sort_records_popup).pack(fill='x', pady=6)
        ttk.Button(nav, text='Export Summary', style='Nav.TButton', command=self.export_summary).pack(fill='x', pady=6)

        ttk.Separator(nav, orient='horizontal').pack(fill='x', pady=8)
        ttk.Label(nav, text='Quick Actions', font=('Segoe UI', 9)).pack(pady=(6,2))
        ttk.Button(nav, text='Refresh Table', command=self.refresh_table).pack(fill='x')

        center = ttk.Frame(container)
        center.pack(side='left', fill='both', expand=True)

        columns = ("id","name","cw_total","exam","total","percentage","grade")
        self.tree = ttk.Treeview(center, columns=columns, show='headings', selectmode='browse')
        for col, text in zip(columns, ['Student ID','Name','CW Total (60)','Exam (100)','Total (160)','Overall %','Grade']):
            self.tree.heading(col, text=text)

        self.tree.column('id', width=90, anchor='center')
        self.tree.column('name', width=180)
        self.tree.column('cw_total', width=100, anchor='center')
        self.tree.column('exam', width=100, anchor='center')
        self.tree.column('total', width=100, anchor='center')
        self.tree.column('percentage', width=90, anchor='center')
        self.tree.column('grade', width=70, anchor='center')

        self.tree.pack(fill='both', expand=True, side='left')

        scrollbar = ttk.Scrollbar(center, orient='vertical', command=self.tree.yview)
        scrollbar.pack(side='left', fill='y')
        self.tree.configure(yscrollcommand=scrollbar.set)

    def load_file(self, filename, silent=False):
        if not os.path.exists(filename):
            if not silent:
                messagebox.showerror('File Error', f'Could not find \n{filename} in this folder.')
            return False
        try:
            with open(filename, 'r', encoding='utf-8') as fh:
                lines = [ln.strip() for ln in fh if ln.strip()]
            idx = 0
            try:
                declared = int(lines[0])
                self.total_students_declared = declared
                idx = 1
            except Exception:
                self.total_students_declared = None
                idx = 0
            self.students = []
            for line in lines[idx:]:
                parts = [p.strip() for p in line.split(',')]
                if len(parts) < 6:
                    continue
                sid = parts[0]
                name = parts[1]
                try:
                    cw1, cw2, cw3 = map(int, parts[2:5])
                    exam = int(parts[5])
                except ValueError:
                    continue
                cw_total = cw1+cw2+cw3
                total = cw_total + exam
                percentage = (total / 160.0) * 100.0
                grade = 'A' if percentage>=70 else 'B' if percentage>=60 else 'C' if percentage>=50 else 'D' if percentage>=40 else 'F'
                record = {'student_id':sid,'student_name':name,'cw_total':cw_total,'exam':exam,'total':total,'percentage':percentage,'grade':grade}
                self.students.append(record)
            self.refresh_table()
            if not silent:
                messagebox.showinfo('Loaded', f'Loaded {len(self.students)} records from {filename}.')
            return True
        except Exception as e:
            messagebox.showerror('Parse Error', f'Failed to read file:\n{e}')
            return False

    def refresh_table(self, data=None, highlight_id=None):
        items = self.tree.get_children()
        for row in items:
            self.tree.delete(row)
        display_data = data if data is not None else self.students
        for rec in display_data:
            self.tree.insert('', 'end', values=(rec['student_id'], rec['student_name'], rec['cw_total'], rec['exam'], rec['total'], f"{rec['percentage']:.2f}", rec['grade']))
        if highlight_id:
            for idx, item in enumerate(self.tree.get_children()):
                if self.tree.item(item,'values')[0]==highlight_id:
                    self.tree.move(item, '', 0)
                    self.tree.selection_set(item)
                    self.tree.see(item)
                    self.tree.item(item, tags=('highlight',))
                    self.tree.tag_configure('highlight', background='yellow')
                    break

    def display_all(self):
        self.refresh_table()
        messagebox.showinfo('Display', 'Showing all loaded student records in the table.')

    def find_student_popup(self):
        sid = simpledialog.askstring('Search', 'Enter student ID to search:')
        if not sid:
            return
        rec = next((s for s in self.students if s['student_id']==sid.strip()), None)
        if rec:
            self.refresh_table(highlight_id=rec['student_id'])
        else:
            messagebox.showwarning('Not Found', f'Student ID {sid} not found.')

    def add_student(self):
        sid = simpledialog.askstring('Add', 'Enter new Student ID:')
        if not sid: return
        name = simpledialog.askstring('Add', 'Enter Student Name:')
        if not name: return
        try:
            cw1 = int(simpledialog.askstring('Add', 'Enter CW1 mark:'))
            cw2 = int(simpledialog.askstring('Add', 'Enter CW2 mark:'))
            cw3 = int(simpledialog.askstring('Add', 'Enter CW3 mark:'))
            exam = int(simpledialog.askstring('Add', 'Enter Exam mark:'))
        except Exception:
            messagebox.showerror('Invalid', 'Marks must be numbers')
            return
        cw_total = cw1+cw2+cw3
        total = cw_total + exam
        pct = total/160*100
        grade = 'A' if pct>=70 else 'B' if pct>=60 else 'C' if pct>=50 else 'D' if pct>=40 else 'F'
        rec = {'student_id':sid,'student_name':name,'cw_total':cw_total,'exam':exam,'total':total,'percentage':pct,'grade':grade}
        self.students.append(rec)
        self.refresh_table()

    def update_student_popup(self):
        sid = simpledialog.askstring('Update', 'Enter Student ID to update:')
        if not sid: return
        rec = next((s for s in self.students if s['student_id']==sid.strip()), None)
        if not rec:
            messagebox.showerror('Not Found','Student not found')
            return
        name = simpledialog.askstring('Update','Enter new name:',initialvalue=rec['student_name'])
        if name: rec['student_name']=name
        try:
            cw1=int(simpledialog.askstring('Update','Enter CW1 mark:',initialvalue=str(rec['cw_total']//3)))
            cw2=int(simpledialog.askstring('Update','Enter CW2 mark:',initialvalue=str(rec['cw_total']//3)))
            cw3=int(simpledialog.askstring('Update','Enter CW3 mark:',initialvalue=str(rec['cw_total']//3)))
            exam=int(simpledialog.askstring('Update','Enter Exam mark:',initialvalue=str(rec['exam'])))
        except: return
        rec['cw_total']=cw1+cw2+cw3
        rec['exam']=exam
        rec['total']=rec['cw_total']+exam
        pct=rec['total']/160*100
        rec['percentage']=pct
        rec['grade']='A' if pct>=70 else 'B' if pct>=60 else 'C' if pct>=50 else 'D' if pct>=40 else 'F'
        self.refresh_table()

    def delete_student_popup(self):
        sid = simpledialog.askstring('Delete', 'Enter Student ID to delete:')
        if not sid: return
        rec = next((s for s in self.students if s['student_id']==sid.strip()), None)
        if not rec:
            messagebox.showerror('Not Found','Student not found')
            return
        self.students.remove(rec)
        self.refresh_table()

    def highest_score(self):
        if not self.students:
            messagebox.showinfo('Info','No students to evaluate.')
            return
        top = max(self.students, key=lambda x: x['percentage'])
        self.refresh_table(highlight_id=top['student_id'])

    def lowest_score(self):
        if not self.students:
            messagebox.showinfo('Info','No students to evaluate.')
            return
        low = min(self.students, key=lambda x: x['percentage'])
        self.refresh_table(highlight_id=low['student_id'])

    def _filter_by_grade_popup(self):
        grade = simpledialog.askstring('Filter', 'Enter grade to filter by (A/B/C/D/F):')
        if not grade: return
        grade = grade.strip().upper()
        if grade not in ('A','B','C','D','F'):
            messagebox.showerror('Invalid', 'Please enter a valid grade (A/B/C/D/F).')
            return
        filtered = [s for s in self.students if s['grade']==grade]
        if not filtered:
            messagebox.showinfo('No results', f'No students with grade {grade}.')
            return
        self.refresh_table(filtered)
        messagebox.showinfo('Filtered', f'Showing {len(filtered)} students with grade {grade}.')

    def sort_records_popup(self):
        choice = simpledialog.askstring('Sort', 'Sort by Total % ascending or descending? (asc/desc):')
        if not choice: return
        choice = choice.strip().lower()
        if choice not in ('asc','desc'):
            messagebox.showerror('Invalid', 'Enter "asc" for ascending or "desc" for descending.')
            return
        reverse = True if choice=='desc' else False
        sorted_list = sorted(self.students, key=lambda x: x['percentage'], reverse=reverse)
        self.refresh_table(sorted_list)
        messagebox.showinfo('Sorted', f'Student records sorted by Overall % ({choice}).')

    def export_summary(self):
        if not self.students:
            messagebox.showinfo('No data', 'Load data before exporting.')
            return
        path = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[('CSV','*.csv')], title='Save summary as')
        if not path: return
        try:
            with open(path,'w',newline='',encoding='utf-8') as csvfile:
                writer=csv.writer(csvfile)
                writer.writerow(['ID','Name','CW Total','Exam','Total','Percentage','Grade'])
                for s in self.students:
                    writer.writerow([s['student_id'],s['student_name'],s['cw_total'],s['exam'],s['total'],f"{s['percentage']:.2f}",s['grade']])
            messagebox.showinfo('Exported', f'Summary exported to:\n{path}')
        except Exception as e:
            messagebox.showerror('Export Error', f'Could not write file:\n{e}')

if __name__=='__main__':
    root=tk.Tk()
    app=StudentManagerApp(root)
    root.mainloop()
