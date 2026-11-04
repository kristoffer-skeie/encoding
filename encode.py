# Simple UI for gap encoding a list of numbers and then encoding the gaps
# with Elias gamma, variable byte or Simple-9.
# Run with:  python enode.py

import importlib.util
import os
import tkinter as tk

FOLDER = os.path.dirname(os.path.abspath(__file__))

# The file names contain "-", so they can't be imported with a normal
# import statement. Load them from their file path instead.
def load(file_name):
    spec = importlib.util.spec_from_file_location(file_name[:-3].replace("-", "_"),
                                                  os.path.join(FOLDER, file_name))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

gap = load("gap-encode.py")
gamma = load("elias-gamma.py")
vbyte = load("var-byte.py")
s9 = load("simple9.py")


def encode():
    output.delete("1.0", tk.END)
    try:
        text = entry.get().replace(",", " ")
        numbers = [int(x) for x in text.split()]
        gaps = gap.gap_encode(numbers)
        output.insert(tk.END, "Sorted:  " + str(sorted(numbers)) + "\n")
        output.insert(tk.END, "Gaps:    " + str(gaps) + "\n\n")

        method = choice.get()
        if method == "Elias gamma":
            codes = gamma.elias_gamma_encode(gaps)
        elif method == "Variable byte":
            codes = vbyte.var_byte_encode(gaps)
        else:
            codes = s9.simple9_encode(gaps)

        if method == "Simple-9":
            for word in codes:
                output.insert(tk.END, word[:4] + " " + word[4:] + "\n")
        else:
            for g, code in zip(gaps, codes):
                output.insert(tk.END, str(g).rjust(8) + "  ->  " + code + "\n")

        total = sum(len(c.replace(" ", "")) for c in codes)
        output.insert(tk.END, "\nTotal bits: " + str(total) + "\n")
    except ValueError as error:
        output.insert(tk.END, "Error: " + str(error) + "\n")


window = tk.Tk()
window.title("Gap Encoder")

tk.Label(window, text="Numbers (separated by space or comma):").pack(anchor="w", padx=10, pady=(10, 0))
entry = tk.Entry(window, width=60)
entry.pack(padx=10, pady=5, fill="x")
entry.insert(0, "3 7 11 23 29 36 40")

choice = tk.StringVar(value="Elias gamma")
row = tk.Frame(window)
row.pack(anchor="w", padx=10)
for name in ["Elias gamma", "Variable byte", "Simple-9"]:
    tk.Radiobutton(row, text=name, variable=choice, value=name).pack(side="left")

tk.Button(window, text="Encode", command=encode).pack(padx=10, pady=5, anchor="w")

output = tk.Text(window, width=70, height=20, font=("Courier", 10))
output.pack(padx=10, pady=(0, 10), fill="both", expand=True)

window.mainloop()
