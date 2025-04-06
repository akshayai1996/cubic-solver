import cmath
from tkinter import Tk, Label, Entry, Button, messagebox

def format_root(root):
    real_part = root.real
    imag_part = root.imag
    if imag_part == 0:
        return f"{real_part:.4g}"
    elif real_part == 0:
        return f"{imag_part:.4g}i"
    else:
        sign = '+' if imag_part > 0 else ''
        return f"{real_part:.4g}{sign}{imag_part:.4g}i"

def solve_cubic():
    try:
        a = float(entry_a.get())
        b = float(entry_b.get())
        c = float(entry_c.get())
        d = float(entry_d.get())

        equation_str = f"{a}x^3 + {b}x^2 + {c}x + {d} = 0"
        label_equation.config(text=f"The equation is: {equation_str}")

        if a == 0:  # Handle quadratic or linear cases
            if b == 0:
                if c == 0:
                    raise ValueError("Invalid equation. Coefficients 'a', 'b', and 'c' cannot all be zero.")
                else:  # Linear case: cx + d = 0
                    root1 = -d / c
                    label_result.config(text=f"Root: {format_root(root1)}")
                    return
            else:  # Quadratic case: bx² + cx + d = 0
                discriminant = c**2 - 4*b*d
                if discriminant < 0:
                    root1 = complex(-c / (2*b), cmath.sqrt(-discriminant) / (2*b))
                    root2 = complex(-c / (2*b), -cmath.sqrt(-discriminant) / (2*b))
                else:
                    root1 = (-c + cmath.sqrt(discriminant)) / (2*b)
                    root2 = (-c - cmath.sqrt(discriminant)) / (2*b)
                label_result.config(text=f"Roots: {format_root(root1)}, {format_root(root2)}")
                return

        # Cubic equation: ax³ + bx² + cx + d = 0
        # Transform to depressed cubic form: t³ + pt + q = 0
        delta0 = b**2 - 3*a*c
        delta1 = 2*b**3 - 9*a*b*c + 27*a**2*d
        discriminant = delta1**2 - 4*delta0**3

        if discriminant > 0:  # One real root and two complex conjugate roots
            C = ((delta1 + cmath.sqrt(discriminant)) / 2)**(1/3)
            u = [1, (-1 + cmath.sqrt(3)*1j) / 2, (-1 - cmath.sqrt(3)*1j) / 2]
            roots = [-(b + u[i]*C + delta0/(u[i]*C)) / (3*a) for i in range(3)]
        elif discriminant == 0:  # All roots real, at least two are equal
            if delta0 == 0:
                roots = [-b / (3*a)]
            else:
                C = (delta1 / 2)**(1/3)
                roots = [-(b + C + delta0/C) / (3*a), -(b + C + delta0/C) / (3*a)]
        else:  # All roots real and distinct
            theta = cmath.acos(delta1 / (2 * cmath.sqrt(delta0**3)))
            roots = [-(b + 2 * cmath.sqrt(delta0) * cmath.cos(theta/3)) / (3*a),
                     -(b + 2 * cmath.sqrt(delta0) * cmath.cos((theta + 2*cmath.pi)/3)) / (3*a),
                     -(b + 2 * cmath.sqrt(delta0) * cmath.cos((theta + 4*cmath.pi)/3)) / (3*a)]

        label_result.config(text=f"Roots: {', '.join(format_root(root) for root in roots)}")

    except ValueError as e:
        messagebox.showerror("Error", str(e))
    except Exception as e:
        messagebox.showerror("Error", f"Invalid input. Please enter valid numbers. Details: {str(e)}")

# GUI setup
root = Tk()
root.title("Cubic Equation Solver")
root.geometry("400x300")
root.configure(bg="#f0f0f0")

Label(root, text="ax³ + bx² + cx + d = 0", font=("Helvetica", 16, "bold"), bg="#f0f0f0").grid(row=0, column=0, columnspan=2, pady=10)

label_equation = Label(root, text="", font=("Helvetica", 12), bg="#f0f0f0")
label_equation.grid(row=1, column=0, columnspan=2, pady=5)

Label(root, text="Coefficient a:", font=("Helvetica", 12), bg="#f0f0f0").grid(row=2, column=0, padx=10, pady=5, sticky="e")
entry_a = Entry(root, font=("Helvetica", 12))
entry_a.grid(row=2, column=1, padx=10, pady=5)

Label(root, text="Coefficient b:", font=("Helvetica", 12), bg="#f0f0f0").grid(row=3, column=0, padx=10, pady=5, sticky="e")
entry_b = Entry(root, font=("Helvetica", 12))
entry_b.grid(row=3, column=1, padx=10, pady=5)

Label(root, text="Coefficient c:", font=("Helvetica", 12), bg="#f0f0f0").grid(row=4, column=0, padx=10, pady=5, sticky="e")
entry_c = Entry(root, font=("Helvetica", 12))
entry_c.grid(row=4, column=1, padx=10, pady=5)

Label(root, text="Constant d:", font=("Helvetica", 12), bg="#f0f0f0").grid(row=5, column=0, padx=10, pady=5, sticky="e")
entry_d = Entry(root, font=("Helvetica", 12))
entry_d.grid(row=5, column=1, padx=10, pady=5)

Button(root, text="Solve Cubic Equation", font=("Helvetica", 12), command=solve_cubic).grid(row=6, column=0, columnspan=2, pady=10)

label_result = Label(root, text="", font=("Helvetica", 12), bg="#f0f0f0")
label_result.grid(row=7, column=0, columnspan=2, pady=5)

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

root.mainloop()