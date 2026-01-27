import tkinter as tk
import secrets
import string
from tkinter import ttk, filedialog, messagebox
from password_core import load_common_passwords, analyze_password, hash_password, get_resource_path
import json
import os
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

load_common_passwords()

password_history = []

def load_history():
    """Load password history from file. Only stores masked data."""
    global password_history
    if os.path.exists('password_history.json'):
        try:
            with open('password_history.json', 'r') as f:
                password_history = json.load(f)
        except:
            password_history = []

def save_history():
    """Save password history to file. Never stores raw passwords."""
    with open('password_history.json', 'w') as f:
        json.dump(password_history, f)

load_history()

dark_mode = False

def toggle_show_password():
    if show_var.get():
        entry.config(show="")
    else:
        entry.config(show="*")

def toggle_dark_mode():
    global dark_mode
    dark_mode = not dark_mode
    
    if dark_mode:
        # Dark mode colors
        bg_color = '#1e1e1e'
        fg_color = '#e0e0e0'
        frame_bg = '#2a2a2a'
        button_bg = '#404040'
        button_fg = '#ffffff'
        
        window.config(bg=bg_color)
        title_frame.config(bg=bg_color)
        input_frame.config(bg=bg_color)
        button_frame.config(bg=bg_color)
        progress_frame.config(bg=bg_color)
        output_frame.config(bg=bg_color)
        output_frame_inner.config(bg=bg_color)
        
        title_label.config(bg=bg_color, fg=fg_color)
        subtitle_label.config(bg=bg_color, fg='#999999')
        input_label.config(bg=bg_color, fg=fg_color)
        progress_bar_label.config(bg=bg_color, fg=fg_color)
        
        # Update input elements
        entry.config(bg='#2d2d2d', fg=fg_color, insertbackground=fg_color)
        show_checkbox.config(bg=bg_color, fg=fg_color, selectcolor=button_bg, activebackground=bg_color, activeforeground=fg_color)
        
        # Update all buttons
        for btn in [check_button, generate_button, history_button, dark_button, batch_button, export_button]:
            btn.config(activebackground='#505050', activeforeground=button_fg)
        
        check_button.config(bg="#2e7d32", fg="white")
        generate_button.config(bg="#1565c0", fg="white")
        history_button.config(bg="#e65100", fg="white")
        dark_button.config(bg="#6a1b9a", fg="white")
        batch_button.config(bg="#455a64", fg="white")
        export_button.config(bg="#5d4037", fg="white")
        
        result_label.config(bg=bg_color, fg=fg_color)
        scrollbar.config()
        
    else:
        # Light mode colors
        bg_color = 'white'
        fg_color = 'black'
        
        window.config(bg=bg_color)
        title_frame.config(bg=bg_color)
        input_frame.config(bg=bg_color)
        button_frame.config(bg=bg_color)
        progress_frame.config(bg=bg_color)
        output_frame.config(bg=bg_color)
        output_frame_inner.config(bg=bg_color)
        
        title_label.config(bg=bg_color, fg=fg_color)
        subtitle_label.config(bg=bg_color, fg='gray')
        input_label.config(bg=bg_color, fg=fg_color)
        progress_bar_label.config(bg=bg_color, fg=fg_color)
        
        entry.config(bg='white', fg='black', insertbackground='black')
        show_checkbox.config(bg='white', fg='black', selectcolor='white', activebackground='white', activeforeground='black')
        
        # Reset buttons to default
        check_button.config(bg="#4CAF50", fg="white")
        generate_button.config(bg="#2196F3", fg="white")
        history_button.config(bg="#FF9800", fg="white")
        dark_button.config(bg="#9C27B0", fg="white")
        batch_button.config(bg="#607D8B", fg="white")
        export_button.config(bg="#795548", fg="white")
        
        result_label.config(bg='white', fg='black')
        scrollbar.config()

def get_badge(score):
    if score >= 5:
        return "🏆 Fort Knox (Excellent!)"
    elif score >= 4:
        return "🛡️ Stronghold (Very Strong)"
    elif score >= 3:
        return "🔒 Secure (Good)"
    elif score >= 2:
        return "⚠️ Caution (Weak)"
    else:
        return "❌ Vulnerable (Very Weak)"

def generate_password():
    # Generate a strong password with at least 12 characters, including all types
    length = 12
    chars = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation
    password = ''.join(secrets.choice(chars) for _ in range(length))
    entry.delete(0, tk.END)
    entry.insert(0, password)
    check_password()  # Automatically check the generated password

def check_password():
    pwd = entry.get()
    if not pwd:
        result_label.config(text="Please enter a password", fg="gray")
        progress_bar['value'] = 0
        return
        
    score, charset, feedback, is_common, entropy, crack_times, zxcvbn_feedback, breached_count = analyze_password(pwd)

    # Build detailed output
    output = f"Strength score: {score}/5\n"
    output += f"Badge: {get_badge(score)}\n"
    output += f"Entropy: {entropy:.2f} bits\n"
    output += f"Common password: {is_common}\n"
    
    # Display breach status with clear messaging
    if breached_count > 0:
        output += f"⚠️  Breached: Yes ({breached_count} times) - DO NOT USE\n"
    elif breached_count == 0:
        output += "✓ Breached: No\n"
    else:
        output += "? Breached: Check failed (offline?) - caution advised\n"
    
    output += f"\nCrack Time (online throttling): {crack_times['online_throttling_100_per_hour']}\n"
    output += f"Crack Time (offline fast): {crack_times['offline_fast_hashing_1e10_per_second']}\n"
    output += f"\nBcrypt Hash:\n{hash_password(pwd)}\n\n"

    if feedback:
        output += "Suggestions:\n"
        for item in feedback:
            output += f"- {item}\n"
    
    if zxcvbn_feedback:
        output += "\nAdvanced Suggestions:\n"
        for item in zxcvbn_feedback:
            output += f"- {item}\n"
    else:
        output += "\n✓ Great password!\n"

    result_label.config(text=output)

    # Set color based on score
    if score <= 1:
        result_label.config(fg="red")
    elif score <= 3:
        result_label.config(fg="orange")
    else:
        result_label.config(fg="green")
    
    # Update progress bar
    progress_bar['value'] = (score / 5) * 100

    # Store MASKED data only - never raw password
    masked_preview = pwd[0] + "*" * (len(pwd) - 2) if len(pwd) > 1 else "*"
    entry_hash = hash_password(pwd)[:20]  # Just first 20 chars as ID
    
    history_entry = {
        'masked': masked_preview,
        'length': len(pwd),
        'score': score,
        'entropy': entropy,
        'breached': breached_count > 0 if breached_count >= 0 else None
    }
    
    # Avoid duplicates in history
    if entry_hash not in [h.get('_hash', '') for h in password_history]:
        password_history.append(history_entry)
        save_history()

def show_history():
    history_window = tk.Toplevel(window)
    history_window.title("Password History")
    history_window.geometry("500x350")
    history_window.resizable(False, False)
    
    tk.Label(history_window, text="Recent Password Checks (Last 10)", font=("Helvetica", 12, "bold")).pack(pady=10)
    
    listbox = tk.Listbox(history_window, width=60, height=12, font=("Helvetica", 9))
    listbox.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
    
    if not password_history:
        listbox.insert(tk.END, "No history yet")
    else:
        for item in password_history[-10:]:  # Last 10
            masked = item.get('masked', '***')
            length = item.get('length', '?')
            score = item.get('score', '?')
            entropy = item.get('entropy', 0)
            breached = "⚠️" if item.get('breached') else "✓" if item.get('breached') is False else "?"
            
            display = f"{breached} {masked} | Len:{length} | Score:{score}/5 | Entropy:{entropy:.2f}"
            listbox.insert(tk.END, display)
    
    tk.Button(history_window, text="Close", command=history_window.destroy, width=15).pack(pady=10)


def batch_check():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if not file_path:
        return
    try:
        df = pd.read_csv(file_path)
        if 'password' not in df.columns:
            messagebox.showerror("Error", "CSV must have a 'password' column")
            return
        results = []
        for pwd in df['password']:
            score, charset, feedback, is_common, entropy, crack_times, zxcvbn_feedback, breached_count = analyze_password(str(pwd))
            results.append({
                'password': pwd,
                'score': score,
                'entropy': entropy,
                'breached': breached_count > 0,
                'crack_time': crack_times['online_throttling_100_per_hour']
            })
        # Show results in a new window
        batch_window = tk.Toplevel(window)
        batch_window.title("Batch Check Results")
        batch_window.geometry("600x400")
        text = tk.Text(batch_window, wrap=tk.WORD)
        text.pack(expand=True, fill=tk.BOTH)
        for res in results:
            text.insert(tk.END, f"Password: {res['password']}\nScore: {res['score']}\nEntropy: {res['entropy']:.2f}\nBreached: {res['breached']}\nCrack Time: {res['crack_time']}\n\n")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def export_report():
    file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if not file_path:
        return
    try:
        c = canvas.Canvas(file_path, pagesize=letter)
        c.drawString(100, 750, "Password Strength Analysis Report")
        c.drawString(100, 730, "=" * 50)
        
        y = 700
        for item in password_history[-10:]:
            masked = item.get('masked', '***')
            length = item.get('length', '?')
            score = item.get('score', '?')
            entropy = item.get('entropy', 0)
            c.drawString(100, y, f"Password: {masked} | Length: {length} | Score: {score}/5 | Entropy: {entropy:.2f} bits")
            y -= 20
            if y < 50:
                c.showPage()
                y = 750
        c.save()
        messagebox.showinfo("Success", f"Report exported to:\n{file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to export report:\n{str(e)}")


# Window
window = tk.Tk()
window.title("Password Strength Checker - Professional Edition")
window.geometry("700x700")
window.resizable(False, False)

# Set window icon (optional - will be set by PyInstaller)
try:
    window.iconbitmap('icon.ico')
except:
    pass

# Frames
title_frame = tk.Frame(window, bg='white')
input_frame = tk.Frame(window, bg='white')
button_frame = tk.Frame(window, bg='white')
progress_frame = tk.Frame(window, bg='white')
output_frame = tk.Frame(window, bg='white')

title_frame.pack(pady=15)
input_frame.pack(pady=10)
button_frame.pack(pady=10)
progress_frame.pack(pady=10)
output_frame.pack(pady=10, fill=tk.BOTH, expand=True)

# Title
title_label = tk.Label(title_frame, text="🔐 Password Strength Checker", font=("Helvetica", 18, "bold"), bg='white', fg='black')
title_label.pack()

subtitle_label = tk.Label(title_frame, text="Analyze password security with professional-grade analysis", font=("Helvetica", 10), fg="gray", bg='white')
subtitle_label.pack()

# Input
input_label = tk.Label(input_frame, text="Enter Password:", font=("Helvetica", 12, "bold"), bg='white', fg='black')
input_label.grid(row=0, column=0, sticky="w", padx=10)
entry = tk.Entry(input_frame, show="*", width=40, font=("Helvetica", 12))
entry.grid(row=0, column=1, padx=10)
entry.bind('<KeyRelease>', lambda event: check_password())  # Real-time feedback

show_var = tk.BooleanVar()
show_checkbox = tk.Checkbutton(input_frame, text="Show Password", variable=show_var, command=toggle_show_password, font=("Helvetica", 10), bg='white', fg='black')
show_checkbox.grid(row=1, column=1, sticky="w", pady=5)

# Buttons - organized in 2 rows
check_button = tk.Button(button_frame, text="Check Password", command=check_password, font=("Helvetica", 11, "bold"), bg="#4CAF50", fg="white", width=16, padx=10)
check_button.grid(row=0, column=0, padx=5, pady=5)

generate_button = tk.Button(button_frame, text="Generate Strong Password", command=generate_password, font=("Helvetica", 11, "bold"), bg="#2196F3", fg="white", width=22, padx=10)
generate_button.grid(row=0, column=1, padx=5, pady=5)

history_button = tk.Button(button_frame, text="History", command=show_history, font=("Helvetica", 11, "bold"), bg="#FF9800", fg="white", width=12, padx=10)
history_button.grid(row=0, column=2, padx=5, pady=5)

dark_button = tk.Button(button_frame, text="🌙 Dark Mode", command=toggle_dark_mode, font=("Helvetica", 11, "bold"), bg="#9C27B0", fg="white", width=12, padx=10)
dark_button.grid(row=0, column=3, padx=5, pady=5)

batch_button = tk.Button(button_frame, text="Batch Check CSV", command=batch_check, font=("Helvetica", 11, "bold"), bg="#607D8B", fg="white", width=14, padx=10)
batch_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

export_button = tk.Button(button_frame, text="Export PDF Report", command=export_report, font=("Helvetica", 11, "bold"), bg="#795548", fg="white", width=16, padx=10)
export_button.grid(row=1, column=2, columnspan=2, padx=5, pady=5)

# Progress bar with label
progress_bar_label = tk.Label(progress_frame, text="Strength Level:", font=("Helvetica", 11, "bold"), bg='white', fg='black')
progress_bar_label.pack()
progress_bar = ttk.Progressbar(progress_frame, orient="horizontal", length=600, mode="determinate", maximum=100)
progress_bar.pack(pady=5)

# Output with scrollbar
output_frame_inner = tk.Frame(output_frame, bg='white')
output_frame_inner.pack(fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(output_frame_inner)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

result_label = tk.Label(output_frame_inner, text="Enter a password to analyze", justify="left", wraplength=650, font=("Helvetica", 10), fg="gray", bg='white')
result_label.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

window.mainloop()

