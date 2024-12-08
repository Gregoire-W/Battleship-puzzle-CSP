# 🛳️ Solve BattleShip Puzzle with CSP  

## 📖 **Introduction**  
The Battleship Puzzle is a fun and logical grid game. The goal is to place all the ships of varying sizes on the grid according to specific rules:  
- Ships must fit within the grid.  
- Ships cannot touch each other, even diagonally.  
- Row and column clues indicate the number of ship cells they must contain.  

This project solves the Battleship Puzzle using **Constraint Satisfaction Problems (CSP)**, a powerful AI method. CSP breaks the problem into **variables**, **domains**, and **constraints** to systematically find solutions.  

---

## 📚 **Table of Contents**  
1. [Features](#features)  
2. [Screenshots or Demo](#screenshots-or-demo)  
3. [Installation](#installation)  
4. [Usage](#usage)  
5. [Technologies Used](#technologies-used)  
6. [Contact Information](#contact-information)  

---
<a name="features"></a>
## 🚀 **Features**  
This project uses CSP to solve the Battleship Puzzle. Here's how it works:  

### 🛠️ **CSP Approach**  
- **Variable**: Each cell of the grid is treated as a variable  
- **Domain**: Each variable can represent a type of boat (0 for water, 1 for submarines, 2 for destroyers, 3 for carriers, 4 for battleships).  
- **Constraints**:  
  1. **Unique Constraints**  
     - **Border Constraints**:  
       - Each cell should have `0 (water)` as diagonal and only the same type of boat next to it.  
     - **M Constraints**:  
       - If there's an `M` in the grid, among the four neighboring cells, two must form a boat, and the rest must be water.  
  2. **Global Constraints**  
     - **Boat Number**: Ensures the correct number of each boat type is placed.  
     - **Boat Size**: Validates that boats have the correct size.  
     - **Global Cardinality**: Ensures row and column constraints match the initial grid's hints.  

### ⚡ **Enhancements with Heuristics and Methods**  
To improve the solving process:  
- **Heuristics**  
  - **MRV (Minimum Remaining Values)**: Select variables with the fewest possible values first.  
  - **LCV (Least Constraining Value)**: Choose values that leave the most options open for other variables.  
  - **Max Degree**: Prioritize variables that interact with the most constraints.  
- **Methods**  
  - **AC-3**: Ensures arc-consistency, simplifying domains.  
  - **Forward Check**: Prunes invalid values before diving into deeper recursion.  

### 📊 **Metrics and Output**  
- Analyze the CSP's efficiency with various metrics.  
- Display or save the puzzle's solution for further study or visualization.  

---
<a name="screenshots-or-demo"></a>
## 📸 **Screenshots or Demo**  
_(Coming Soon!)_  

---
<a name="installation"></a>
## 💻 **Installation**  
Clone the repository and run the program:  
```bash  
git clone <repository-url>  
cd battleship-csp  
python main.py
```
---
<a name="usage"></a>
## 🔧 **Usage**  
This project is adaptable for solving other CSP problems. To use it:  
1. Define new **variables**, **domains**, and **constraints**.  
2. Leverage the existing CSP logic for computation.  
3. Metrics and heuristics are built-in and reusable!  

---
<a name="technologies-used"></a>
## 🛠️ **Technologies Used**  
- **Python**: Programming language.   

---
<a name="contact-information"></a>
## 📬 **Contact Information**  
For questions or support, feel free to reach out:  
**Email**: gregoire.woroniak@gmail.com  
