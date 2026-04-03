import tkinter as tk
from tkinter import ttk
import time

class VisualNode:
    def __init__(self, canvas, id, val, x, y):
        self.canvas = canvas
        self.id = id
        self.val = val
        self.x = x
        self.y = y
        self.target_x = x
        self.target_y = y
        self.original_y = y
        self.width = 60
        self.height = 40
        self.color = "#87CEFA"
        
        self.rect = self.canvas.create_rectangle(x, y, x + self.width, y + self.height, fill=self.color, outline="black", width=2)
        self.line = self.canvas.create_line(x + self.width*0.7, y, x + self.width*0.7, y + self.height, fill="black", width=2)
        self.text = self.canvas.create_text(x + self.width*0.35, y + self.height/2, text=str(val), font=("Arial", 12, "bold"))
        self.next_node = None

    def update_position(self):
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        self.x += dx * 0.2
        self.y += dy * 0.2
        self.canvas.coords(self.rect, self.x, self.y, self.x + self.width, self.y + self.height)
        self.canvas.coords(self.line, self.x + self.width*0.7, self.y, self.x + self.width*0.7, self.y + self.height)
        self.canvas.coords(self.text, self.x + self.width*0.35, self.y + self.height/2)

    def set_color(self, color):
        self.color = color
        self.canvas.itemconfig(self.rect, fill=color)

    def jump_and_highlight(self):
        self.set_color("#FF5252")
        self.target_y = self.original_y - 40
        self.canvas.after(200, lambda: setattr(self, 'target_y', self.original_y + 10))
        self.canvas.after(350, lambda: setattr(self, 'target_y', self.original_y))
        self.canvas.after(800, lambda: self.set_color("#87CEFA"))

class VariablePointer:
    def __init__(self, canvas, name, x, y, color):
        self.canvas = canvas
        self.name = name
        self.x = x
        self.y = y
        self.target_x = x
        self.target_y = y
        self.color = color
        self.target_node = None
        self.text = self.canvas.create_text(x, y, text=name, font=("Consolas", 12, "bold"), fill=color)
        self.arrow = self.canvas.create_line(x, y+10, x, y+30, arrow=tk.LAST, fill=color, width=3)

    def point_to(self, target_node, offset_y=-40):
        self.target_node = target_node
        if target_node is None:
            self.target_x = -100
            self.target_y = -100
        else:
            self.target_x = target_node.x + target_node.width/2
            self.target_y = target_node.y + offset_y

    def update_position(self):
        if self.target_node:
            self.target_x = self.target_node.x + self.target_node.width/2
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        if abs(dx) > 0.5 or abs(dy) > 0.5:
            self.x += dx * 0.15
            self.y += dy * 0.15
        self.canvas.coords(self.text, self.x, self.y)
        self.canvas.coords(self.arrow, self.x, self.y+10, self.x, self.y+35)

    def set_label(self, new_name):
        self.name = new_name
        self.canvas.itemconfig(self.text, text=new_name)

class CurvedArrow:
    def __init__(self, canvas, start_node, end_node=None):
        self.canvas = canvas
        self.start_node = start_node
        self.end_node = end_node
        self.line = self.canvas.create_line(0,0,0,0, arrow=tk.LAST, width=3, fill="#333", smooth=True)
        
    def update_position(self):
        if self.start_node is None:
            self.canvas.coords(self.line, -50,-50,-50,-50)
            return

        sx = self.start_node.x + self.start_node.width * 0.85
        sy = self.start_node.y + self.start_node.height / 2
        
        if self.end_node is None:
            self.canvas.coords(self.line, sx, sy, sx + 20, sy + 40)
            self.canvas.itemconfig(self.line, arrow=tk.NONE, dash=(4,4), fill="#999")
        else:
            self.canvas.itemconfig(self.line, arrow=tk.LAST, dash=(), fill="#333")
            ex = self.end_node.x
            ey = self.end_node.y + self.end_node.height / 2
            
            if ex < sx:
                cx1 = sx + 20; cy1 = sy + 60
                cx2 = ex - 20; cy2 = ey + 60
                self.canvas.coords(self.line, sx, sy, cx1, cy1, cx2, cy2, ex, ey)
            else:
                self.canvas.coords(self.line, sx, sy, (sx+ex)/2, (sy+ey)/2, ex, ey)

class LinkedListVisualizer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("통합 연결 리스트 시각화 런처 (Q1 ~ Q7)")
        self.geometry("1400x800")
        self.configure(bg="#2E2E2E")
        
        self.nodes = []
        self.arrows = []
        self.variables = {}
        self.call_stack = []
        
        self.is_playing = False
        self.generator = None
        self.current_q = "Q1: insertSortedLL"
        
        self.head_node_ptr = None
        self.head_node_ptr2 = None
        
        self.init_ui()
        self.init_data()
        self.run_animation_loop()

    def init_ui(self):
        top_frame = tk.Frame(self, bg="#1E1E1E", pady=10)
        top_frame.pack(fill=tk.X)
        
        tk.Label(top_frame, text="📂 문제 선택:", font=("맑은 고딕", 12, "bold"), bg="#1E1E1E", fg="#FFF").pack(side=tk.LEFT, padx=10)
        self.q_combobox = ttk.Combobox(top_frame, values=[
            "Q1: insertSortedLL", 
            "Q2: alternateMergeLinkedList", 
            "Q3: moveOddItemsToBack", 
            "Q4: moveEvenItemsToBack", 
            "Q5: frontBackSplitLinkedList", 
            "Q6: moveMaxToFront", 
            "Q7: RecursiveReverse"
        ], font=("맑은 고딕", 11), width=35, state="readonly")
        self.q_combobox.set(self.current_q)
        self.q_combobox.pack(side=tk.LEFT, padx=10)
        self.q_combobox.bind("<<ComboboxSelected>>", self.on_q_change)
        
        control_frame = tk.Frame(self, bg="#333", pady=10)
        control_frame.pack(fill=tk.X)
        
        btn_style = {"font": ("맑은 고딕", 10, "bold"), "bg": "#4CAF50", "fg": "white", "width": 12, "cursor": "hand2"}
        self.btn_next = tk.Button(control_frame, text="다음 스텝 ⏭", command=self.step_forward, **btn_style)
        self.btn_next.pack(side=tk.LEFT, padx=10)
        self.btn_play = tk.Button(control_frame, text="자동 재생 ▶", command=self.toggle_play, bg="#2196F3", font=("맑은 고딕", 10, "bold"), fg="white", width=12, cursor="hand2")
        self.btn_play.pack(side=tk.LEFT, padx=10)
        self.btn_reset = tk.Button(control_frame, text="초기화 ↺", command=self.reset_all, bg="#F44336", font=("맑은 고딕", 10, "bold"), fg="white", width=12, cursor="hand2")
        self.btn_reset.pack(side=tk.LEFT, padx=10)
        
        self.status_var = tk.StringVar()
        self.status_var.set("상태: 대기 중")
        tk.Label(control_frame, textvariable=self.status_var, font=("맑은 고딕", 11), bg="#333", fg="white").pack(side=tk.RIGHT, padx=20)
        
        main_paned = tk.PanedWindow(self, orient=tk.VERTICAL, bg="#2E2E2E")
        main_paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.canvas = tk.Canvas(main_paned, bg="#F5F5F5", highlightthickness=0)
        main_paned.add(self.canvas, minsize=400)
        
        bottom_paned = tk.PanedWindow(main_paned, orient=tk.HORIZONTAL, bg="#2E2E2E")
        main_paned.add(bottom_paned, minsize=250)
        
        left_panel = tk.Frame(bottom_paned, bg="#1E1E1E")
        bottom_paned.add(left_panel, width=550)
        
        desc_frame = tk.Frame(left_panel, bg="#2C3E50", bd=2, relief=tk.GROOVE)
        desc_frame.pack(fill=tk.X, padx=5, pady=5)
        tk.Label(desc_frame, text="💡 코드 해설 (진행 상황)", font=("맑은 고딕", 10, "bold"), bg="#2C3E50", fg="#F1C40F").pack(anchor=tk.W, padx=5, pady=2)
        
        self.desc_text = tk.Text(desc_frame, height=3, font=("맑은 고딕", 12), bg="#34495E", fg="white", wrap=tk.WORD, bd=0, padx=5, pady=5)
        self.desc_text.pack(fill=tk.X)
        self.desc_text.insert(tk.END, "선택된 알고리즘의 동작 과정을 확인하세요.")
        self.desc_text.config(state=tk.DISABLED)

        code_frame = tk.Frame(left_panel, bg="#1E1E1E")
        code_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        tk.Label(code_frame, text="💻 C 소스 코드", font=("맑은 고딕", 10, "bold"), bg="#1E1E1E", fg="#FFF").pack(anchor=tk.W, pady=2)
        
        self.code_text = tk.Text(code_frame, height=12, font=("Consolas", 12), bg="#282C34", fg="#ABB2BF", wrap=tk.NONE)
        self.code_text.pack(fill=tk.BOTH, expand=True)
        self.code_text.tag_config('highlight', background="#3E4451", foreground="#E5C07B")
        
        stack_frame = tk.Frame(bottom_paned, bg="#1E1E1E")
        bottom_paned.add(stack_frame)
        self.stack_label = tk.Label(stack_frame, text="📚 변수 감시창", font=("맑은 고딕", 10, "bold"), bg="#1E1E1E", fg="#FFF")
        self.stack_label.pack(anchor=tk.W, padx=5, pady=5)
        self.stack_canvas = tk.Canvas(stack_frame, bg="#282C34", highlightthickness=0)
        self.stack_canvas.pack(fill=tk.BOTH, expand=True)

    def on_q_change(self, event):
        self.current_q = self.q_combobox.get()
        self.reset_all()

    def update_c_code(self, code_str):
        self.code_text.config(state=tk.NORMAL)
        self.code_text.delete('1.0', tk.END)
        self.code_text.insert(tk.END, code_str)
        self.code_text.config(state=tk.DISABLED)

    def highlight_code(self, line_idx):
        self.code_text.config(state=tk.NORMAL)
        self.code_text.tag_remove('highlight', '1.0', tk.END)
        if line_idx >= 0:
            self.code_text.tag_add('highlight', f'{line_idx+1}.0', f'{line_idx+1}.end')
        self.code_text.config(state=tk.DISABLED)

    def update_description(self, text):
        self.desc_text.config(state=tk.NORMAL)
        self.desc_text.delete('1.0', tk.END)
        self.desc_text.insert(tk.END, text)
        self.desc_text.config(state=tk.DISABLED)

    def draw_stack(self):
        self.stack_canvas.delete("all")
        y = 20
        if "Q7" in self.current_q:
            self.stack_label.config(text="📚 콜 스택 (Call Stack)")
            for i, frame in enumerate(self.call_stack):
                color = "#FFEB3B" if i == len(self.call_stack)-1 else "#E0E0E0"
                self.stack_canvas.create_rectangle(10, y, 220, y+35, fill="#37474F", outline=color, width=2)
                node_val = frame['head'].val if frame['head'] else "NULL"
                depth = frame['depth']
                self.stack_canvas.create_text(115, y+17, text=f"[스택 {depth}층] Reverse({node_val})", fill="white", font=("Consolas", 10, "bold"))
                y += 45
        else:
            self.stack_label.config(text="🔍 현재 로컬 변수 상태")
            y_offset = 20
            for name, ptr in self.variables.items():
                if ptr.target_node:
                    val = ptr.target_node.val
                elif ptr.target_node is None:
                    continue  # if variable hasn't been set, just don't show or show NULL
                else:
                    val = "NULL"
                if ptr.target_node is None:
                    disp = "NULL"
                else: disp = val
                self.stack_canvas.create_text(20, y_offset, text=f"{name} -> {disp}", fill=ptr.color, font=("Consolas", 13, "bold"), anchor="w")
                y_offset += 30

    def create_node(self, val, x, y):
        n = VisualNode(self.canvas, id=len(self.nodes), val=val, x=x, y=y)
        self.nodes.append(n)
        return n

    def create_arrow(self, src, tgt):
        arr = CurvedArrow(self.canvas, src, tgt)
        self.arrows.append(arr)
        if src: src.next_node = tgt
        return arr

    def set_next(self, src, tgt):
        if not src: return
        src.next_node = tgt
        for arr in self.arrows:
            if arr.start_node == src:
                arr.end_node = tgt
                return
        self.create_arrow(src, tgt)

    def force_unlink(self, start_node):
        start_node.next_node = None
        for arr in self.arrows:
            if arr.start_node == start_node:
                arr.end_node = None

    def align_list(self, head, start_x, start_y):
        curr = head
        idx = 0
        visited = set()
        while curr:
            if curr in visited: break # 순환 구조시 탈출
            visited.add(curr)
            curr.target_x = start_x + idx * 100
            curr.target_y = start_y
            curr.original_y = start_y
            curr = curr.next_node
            idx += 1

    def init_data(self):
        self.is_playing = False
        self.canvas.delete("all")
        self.stack_canvas.delete("all")
        self.nodes.clear()
        self.arrows.clear()
        self.variables.clear()
        self.call_stack.clear()
        self.head_node_ptr = None
        self.head_node_ptr2 = None
        
        self.generator = None
        self.status_var.set("상태: 알고리즘 준비됨")
        self.btn_play.config(text="자동 재생 ▶", bg="#2196F3")

        colors = ["#E91E63", "#FF9800", "#4CAF50", "#9C27B0", "#00BCD4"]
        
        if "Q1" in self.current_q:
            c_code = """int insertSortedLL(LinkedList *ll, int item) {
    if (ll == NULL) return -1;
    int index = 0;
    ListNode *cur = ll->head;
    while (cur != NULL && cur->item < item) {
        cur = cur->next;
        index++;
    }
    insertNode(ll, index, item);
    return index;
}"""
            self.update_c_code(c_code)
            arr = [10, 30, 40, 50]
            head = None; prev = None
            for i, v in enumerate(arr):
                n = self.create_node(v, 100 + i*100, 150)
                if not head: head = n
                if prev: self.set_next(prev, n)
                prev = n
            self.set_next(prev, None)
            
            self.head_node_ptr = head
            self.variables["cur"] = VariablePointer(self.canvas, "cur", 50, 50, colors[1])
            self.variables["cur"].point_to(head)
            
            self.new_node = self.create_node(25, -100, 250)
            self.new_node.target_x = 50
            self.new_node.target_y = 250
            self.generator = self.algo_generator_q1()

        elif "Q2" in self.current_q:
            c_code = """void alternateMergeLinkedList(LinkedList *ll1, LinkedList *ll2) {
    ListNode *p1 = ll1->head;
    ListNode *p2 = ll2->head;
    while (p1 != NULL && p2 != NULL) {
        ListNode *next1 = p1->next;
        ListNode *next2 = p2->next;

        p1->next = p2;
        p2->next = next1;

        p1 = next1;
        p2 = next2;
    }
    ll2->head = p2;
}"""
            self.update_c_code(c_code)
            arr1 = [1, 3, 5]
            arr2 = [2, 4, 6]
            h1 = None; prev = None
            for i, v in enumerate(arr1):
                n = self.create_node(v, 100 + i*100, 120)
                if not h1: h1 = n
                if prev: self.set_next(prev, n)
                prev = n
            self.set_next(prev, None)
            h2 = None; prev = None
            for i, v in enumerate(arr2):
                n = self.create_node(v, 100 + i*100, 250)
                if not h2: h2 = n
                if prev: self.set_next(prev, n)
                prev = n
            self.set_next(prev, None)
            
            self.head_node_ptr = h1
            self.head_node_ptr2 = h2
            self.variables["p1"] = VariablePointer(self.canvas, "p1", 50, 50, colors[0])
            self.variables["p2"] = VariablePointer(self.canvas, "p2", 50, 50, colors[1])
            self.generator = self.algo_generator_q2()

        elif "Q3" in self.current_q:
            c_code = """void moveOddItemsToBack(LinkedList *ll) {
    if (ll == NULL || ll->head == NULL) return;
    ListNode *cur = ll->head, *prev = NULL, *tail = ll->head;
    while (tail->next != NULL) tail = tail->next;
    ListNode *oldTail = tail;

    while (cur != NULL && cur != oldTail->next) {
        if (cur->item % 2 != 0) {
            ListNode *nextNode = cur->next;
            if (prev == NULL) ll->head = nextNode;
            else prev->next = nextNode;

            tail->next = cur;
            cur->next = NULL;
            tail = cur;
            cur = nextNode;
        } else {
            prev = cur;
            cur = cur->next;
        }
    }
}"""
            self.update_c_code(c_code)
            arr = [3, 2, 5, 8, 7, 4]
            head = None; prev = None
            for i, v in enumerate(arr):
                n = self.create_node(v, 100 + i*100, 150)
                if not head: head = n
                if prev: self.set_next(prev, n)
                prev = n
            self.set_next(prev, None)
            self.head_node_ptr = head
            self.variables["cur"] = VariablePointer(self.canvas, "cur", 50, 50, colors[0])
            self.variables["prev"] = VariablePointer(self.canvas, "prev", 50, 50, colors[1])
            self.variables["tail"] = VariablePointer(self.canvas, "tail", 50, 50, colors[2])
            self.generator = self.algo_generator_q3(is_even=False)

        elif "Q4" in self.current_q:
            c_code = """void moveEvenItemsToBack(LinkedList *ll) {
    // moveOddItemsToBack 와 동일하며 짝수를 추출합니다
    if (cur->item % 2 == 0) {
        ... // 뒤로 던지기 로직
    } else {
        prev = cur;
        cur = cur->next;
    }
}"""
            self.update_c_code(c_code)
            arr = [4, 5, 2, 7, 8, 3] # Q3과 동일한 구조재사용
            head = None; prev = None
            for i, v in enumerate(arr):
                n = self.create_node(v, 100 + i*100, 150)
                if not head: head = n
                if prev: self.set_next(prev, n)
                prev = n
            self.set_next(prev, None)
            self.head_node_ptr = head
            self.variables["cur"] = VariablePointer(self.canvas, "cur", 50, 50, colors[0])
            self.variables["prev"] = VariablePointer(self.canvas, "prev", 50, 50, colors[1])
            self.variables["tail"] = VariablePointer(self.canvas, "tail", 50, 50, colors[2])
            self.generator = self.algo_generator_q3(is_even=True)

        elif "Q5" in self.current_q:
            c_code = """void frontBackSplitLinkedList(LinkedList *ll, ...) {
    if (ll == NULL || ll->head == NULL) return;
    ListNode *slow = ll->head;
    ListNode *fast = ll->head;
    if (fast->next != NULL) {
        fast = fast->next->next;
    }
    while (fast != NULL) {
        slow = slow->next;
        fast = fast->next;
        if (fast != NULL) fast = fast->next;
    }
    resultFrontList->head = ll->head;
    resultBackList->head = slow->next;
    slow->next = NULL;
}"""
            self.update_c_code(c_code)
            arr = [1, 2, 3, 4, 5, 6, 7]
            head = None; prev = None
            for i, v in enumerate(arr):
                n = self.create_node(v, 100 + i*100, 150)
                if not head: head = n
                if prev: self.set_next(prev, n)
                prev = n
            self.set_next(prev, None)
            self.head_node_ptr = head
            
            self.variables["slow"] = VariablePointer(self.canvas, "거북이(slow)", 50, 50, colors[1])
            self.variables["fast"] = VariablePointer(self.canvas, "토끼(fast)", 50, 50, colors[0])
            self.generator = self.algo_generator_q5()

        elif "Q6" in self.current_q:
            c_code = """int moveMaxToFront(ListNode **ptrHead) {
    ListNode *cur = (*ptrHead)->next;
    ListNode *prev = *ptrHead;
    ListNode *maxNode = *ptrHead;
    ListNode *maxPrev = NULL;
    while (cur != NULL) {
        if (cur->item > maxNode->item) {
            maxNode = cur;
            maxPrev = prev;
        }
        prev = cur;
        cur = cur->next;
    }
    if (maxPrev == NULL) return 0;
    maxPrev->next = maxNode->next;
    maxNode->next = *ptrHead;
    *ptrHead = maxNode;
    return 0;
}"""
            self.update_c_code(c_code)
            arr = [12, 5, 99, 17, 34]
            head = None; prev = None
            for i, v in enumerate(arr):
                n = self.create_node(v, 100 + i*100, 150)
                if not head: head = n
                if prev: self.set_next(prev, n)
                prev = n
            self.set_next(prev, None)
            
            self.head_node_ptr = head
            self.variables["ptrHead"] = VariablePointer(self.canvas, "ptrHead", 50, 50, colors[0])
            self.variables["cur"] = VariablePointer(self.canvas, "cur", 50, 50, colors[1])
            self.variables["prev"] = VariablePointer(self.canvas, "prev", 50, 50, colors[2])
            self.variables["maxNode"] = VariablePointer(self.canvas, "maxNode(👑)", 50, 50, colors[3])
            
            self.variables["ptrHead"].point_to(head)
            self.generator = self.algo_generator_q6()

        elif "Q7" in self.current_q:
            c_code = """void RecursiveReverse(ListNode **ptrHead) {
    ListNode *firstNode, *restOfList;
    if (ptrHead == NULL || *ptrHead == NULL) return;
    firstNode = *ptrHead;
    restOfList = firstNode->next;
    if (restOfList == NULL) return;
    RecursiveReverse(&restOfList);
    firstNode->next->next = firstNode;
    firstNode->next = NULL;
    *ptrHead = restOfList;
}"""
            self.update_c_code(c_code)
            arr = [10, 20, 30, 40]
            head = None; prev = None
            for i, v in enumerate(arr):
                n = self.create_node(v, 100 + i*100, 150)
                if not head: head = n
                if prev: self.set_next(prev, n)
                prev = n
            self.set_next(prev, None)
            
            self.variables["ptrHead"] = VariablePointer(self.canvas, "ptrHead", 50, 50, "#E91E63")
            self.variables["firstNode"] = VariablePointer(self.canvas, "first", 50, 50, "#FF9800")
            self.variables["restOfList"] = VariablePointer(self.canvas, "rest", 50, 50, "#4CAF50")
            self.variables["ptrHead"].point_to(head)
            self.variables["firstNode"].point_to(None)
            self.variables["restOfList"].point_to(None)
            
            self.head_node_ptr = head
            self.generator = self.algo_generator_q7(1, head)

        self.highlight_code(-1)
        self.draw_stack()

    # ========================== Q1: 정렬 삽입 ==========================
    def algo_generator_q1(self):
        head = self.head_node_ptr
        yield {"msg": "초기화", "desc": "새로운 노드(25)를 정렬된 삽입 구조에 맞게 순회하며 위치를 찾습니다.", "line": 0}
        cur = head
        index = 0
        yield {"msg": "탐색 시작", "desc": "cur가 처음(10)부터 차례차례 비교를 시작합니다.", "line": 4, "set_var": "cur", "target": cur}
        while cur and cur.val < self.new_node.val:
            yield {"msg": "조건 비교", "desc": f"현재 {cur.val} < 25 이므로 한 칸 뒤로 이동합니다.", "line": 5, "set_var": "cur", "target": cur}
            cur = cur.next_node
            index += 1
            yield {"msg": "이동 결과", "desc": f"다음 위치 확인 (index={index}).", "line": 6, "set_var": "cur", "target": cur}
        
        yield {"msg": "자리 발견", "desc": f"{cur.val}가 25보다 크므로, 바로 이 자리가 삽입 위치입니다!", "line": 8}
        self.new_node.jump_and_highlight()
        if index == 0:
            self.set_next(self.new_node, head)
            head = self.new_node
        else:
            temp = head
            for _ in range(index-1): temp = temp.next_node
            self.set_next(self.new_node, temp.next_node)
            self.set_next(temp, self.new_node)
        yield {"msg": "삽입 적용", "desc": "새 노드가 기존 노드들 사이를 비집고 파고들어 연결됩니다.", "line": 9, "align": {"head": head, "x": 100, "y": 150}}
        yield {"msg": "종료", "desc": "모든 정렬 삽입 과정 완료.", "line": -1}

    # ========================== Q2: 지퍼 병합 (Alternate) ==========================
    def algo_generator_q2(self):
        p1 = self.head_node_ptr
        p2 = self.head_node_ptr2
        yield {"msg": "초기화", "desc": "p1은 위쪽 리스트, p2는 아래쪽 리스트를 가리킵니다.", "line": 2, "set_var": "p1", "target": p1, "set_var": "p2", "target": p2}
        while p1 and p2:
            next1 = p1.next_node
            next2 = p2.next_node
            yield {"msg": "현재 연결 백업", "desc": "기존 연결이 망가지지 않도록 다음 번지들을 기억해 둡니다.", "line": 6}
            self.set_next(p1, p2)
            yield {"msg": "교차 연결 1", "desc": f"p1({p1.val}) 뒤에 p2({p2.val})를 붙입니다.", "line": 8, "align2_zipped": True}
            self.set_next(p2, next1)
            yield {"msg": "교차 연결 2", "desc": f"p2({p2.val}) 다음에 원래 p1 뒷부분({next1.val if next1 else 'NULL'})을 이웃시킵니다.", "line": 9, "align2_zipped": True}
            p1 = next1
            p2 = next2
            yield {"msg": "다음으로 이동", "desc": "작업을 마친 포인터들이 다시 다음 노드로 진격합니다.", "line": 12, "set_var": "p1", "target": p1, "set_var": "p2", "target": p2}
        
        self.head_node_ptr2 = p2
        yield {"msg": "종료", "desc": "모든 노드가 자크(Zipper)처럼 하나로 병합되었습니다!", "line": -1, "align2_zipped": True}

    # ========================== Q3 / Q4: 짝수 홀수 추출 ==========================
    def algo_generator_q3(self, is_even=False):
        head = self.head_node_ptr
        target_name = "짝수" if is_even else "홀수"
        cur = head
        prev = None
        tail = head
        
        yield {"msg": "초기화", "desc": "맨 끝 꼬리(tail)를 우선 찾으러 갑니다.", "line": 3, "set_var": "tail", "target": tail}
        while tail.next_node: tail = tail.next_node
        oldTail = tail
        yield {"msg": "꼬리 확인", "desc": f"원래 끝 꼬리는 {oldTail.val}입니다. 이 꼬리까지만 검사하면 무한루프를 막을 수 있습니다.", "line": 5, "set_var": "tail", "target": tail}
        
        yield {"msg": "탐색 시작", "desc": f"{target_name}를 매의 눈으로 찾기 시작합니다.", "line": 7, "set_var": "cur", "target": cur, "set_var": "prev", "target": prev}
        while cur and cur != getattr(oldTail, 'next_node', None): # prevent looping past old bounds
            yield {"msg": "검수소 통과", "desc": f"현재 값 {cur.val} 검사 중...", "line": 8, "set_var": "cur", "target": cur}
            # Q4는 짝수 검사, Q3는 홀수 검사
            condition = (cur.val % 2 == 0) if is_even else (cur.val % 2 != 0)
            
            if condition:
                yield {"msg": f"{target_name} 적발!", "desc": f"발견했습니다! {cur.val}을(를) 적발하여 강제로 맨 뒤로 날려보냅니다.", "line": 9, "action": "jump", "target": cur}
                nextNode = cur.next_node
                if prev is None:
                    head = nextNode
                else:
                    self.set_next(prev, nextNode)
                
                self.set_next(tail, cur)
                self.set_next(cur, None)
                tail = cur
                cur = nextNode
                yield {"msg": "후방 배치 완료", "desc": "적발된 노드가 끝 꼬리에 합류했습니다.", "line": 15, "align": {"head": head, "x": 100, "y": 150}, "set_var": "tail", "target": tail}
            else:
                yield {"msg": "무사 통과", "desc": "타겟이 아니므로 그냥 넘어갑니다.", "line": 17}
                prev = cur
                cur = cur.next_node
                
        yield {"msg": "종료", "desc": f"모든 {target_name}들이 후방으로 쫒겨났습니다!", "line": -1, "align": {"head": head, "x": 100, "y": 150}}


    # ========================== Q5: 토끼와 거북이 (Split) ==========================
    def algo_generator_q5(self):
        head = self.head_node_ptr
        slow = head
        fast = head
        
        yield {"msg": "출발선", "desc": "토끼(fast)와 거북이(slow)가 모두 시작점(Head)에서 출발합니다.", "line": 3, "set_var": "slow", "target": slow, "set_var": "fast", "target": fast}
        if fast.next_node:
            fast = fast.next_node.next_node
            yield {"msg": "토끼 준비", "desc": "시작하자마자 토끼는 2칸 먼저 앞서나갑니다.", "line": 5, "set_var": "fast", "target": fast}
            
        while fast:
            yield {"msg": "달리기 반복", "desc": "거북이는 1칸, 토끼는 무려 2칸이나 달립니다. (토끼가 끝에 닿을 때 거북이는 정확히 중간!)", "line": 8}
            slow = slow.next_node
            fast = fast.next_node
            if fast: fast = fast.next_node
            yield {"msg": "트랙 이동", "desc": f"거북이: {slow.val}, 토끼: {fast.val if fast else '트랙 끝 통과!'}", "line": 10, "set_var": "slow", "target": slow, "set_var": "fast", "target": fast}
            
        yield {"msg": "경주 종료", "desc": "토끼가 골인했으므로 거북이 위치가 정확히 리스트의 정중앙 지점입니다.", "line": 14}
        back_head = slow.next_node
        yield {"msg": "단칼에 분할", "desc": "거북이 뒤를 절단내어 frontList와 backList 단 2계파로 나누어 버립니다!", "line": 16}
        self.force_unlink(slow)
        yield {"msg": "정렬 완료", "desc": "리스트가 두 덩어리(Front, Back)로 나뉘어졌습니다.", "line": -1, "align": {"head": head, "x": 100, "y": 100}, "align2": {"head": back_head, "x": 100, "y": 250}}

    # ========================== Q6: 최고값 워프 ==========================
    def algo_generator_q6(self):
        head = self.head_node_ptr
        cur = head.next_node
        prev = head
        maxNode = head
        maxPrev = None
        
        yield {"msg": "왕관 찾기 준비", "desc": "ptrHead부터 제일 큰 값(maxNode👑)이 누군지 순회탐색을 시작합니다.", "line": 3, "set_var": "maxNode", "target": maxNode}
        
        while cur:
            yield {"msg": "새로운 도전자", "desc": f"가장 큰 챔피언({maxNode.val})과 도전자({cur.val})가 비교됩니다.", "line": 7, "set_var": "cur", "target": cur}
            if cur.val > maxNode.val:
                maxNode = cur
                maxPrev = prev
                yield {"msg": "👑 챔피언 교체!!", "desc": f"오오!! 더 큰 상대({maxNode.val})가 등장하며 왕관을 뺏어냅니다!", "line": 10, "set_var": "maxNode", "target": maxNode}
            prev = cur
            cur = cur.next_node
            
        yield {"msg": "최종 군주 확정", "desc": f"심사가 끝났습니다. 최강자는 {maxNode.val} 입니다.", "line": 15}
        if maxPrev is None:
             yield {"msg": "이동할 필요 없음", "desc": "최강자가 원래부터 1번 자리라 바꿀 게 없습니다.", "line": 16}
             return
             
        yield {"msg": "워프 1단계: 적출", "desc": "최강자 노드를 리스트 사이에서 과감하게 쑥! 적출해냅니다.", "line": 17}
        self.set_next(maxPrev, maxNode.next_node)
        
        yield {"msg": "워프 2단계: 최전방 워프", "desc": "맨 앞 헤드에 꽂아 넣어 리더로 삼습니다!", "line": 18}
        self.set_next(maxNode, head)
        head = maxNode
        yield {"msg": "종료", "desc": "왕좌 교체 및 정렬이 완료되었습니다.", "line": -1, "align": {"head": head, "x": 100, "y": 150}}

    # ========================== Q7: 재귀 역전 ==========================
    def algo_generator_q7(self, depth, current_head):
        self.call_stack.append({'head': current_head, 'depth': depth})
        yield {"msg": f"Reverse({current_head.val if current_head else 'NULL'}) 진입", "desc": f"✨ 방 {depth}층 입장! 마술상자에 들어왔습니다.", "line": 0, "stack_update": True, "depth_label": f"firstNode (방 {depth}층 대기)"}
        yield {"msg": "종료 조건 확인", "desc": "빈 리스트 조사 중입니다.", "line": 2}
        if current_head is None:
            self.call_stack.pop(); yield {"msg": "리턴", "desc": "비어있군요, 이전 방으로 돌아가세요.", "line": 3, "stack_update": True}
            return current_head
            
        first_node = current_head
        yield {"msg": "주인공 등장", "desc": f"이 층에서는 {first_node.val}가 'firstNode(주황색)' 입니다.", "line": 4, "set_var": "firstNode", "target": first_node, "depth_label": f"firstNode (방 {depth}층)"}
        
        rest_of_list = first_node.next_node
        if rest_of_list is None:
            self.call_stack.pop(); yield {"msg": "단일 꼬리 반환", "desc": "꼬리 끝입니다! 여기서부터 도로 말려올라갑니다.", "line": 6, "stack_update": True}
            return first_node
            
        sub_gen = self.algo_generator_q7(depth + 1, rest_of_list)
        new_head = None
        try:
            while True: yield next(sub_gen)
        except StopIteration as e: new_head = e.value
            
        yield {"msg": f"방 {depth}층 복귀", "desc": f"🔥 기상 라팔! 이 방의 당당한 주인공 {first_node.val}가 깨어나 통통 튑니다!", "line": 7, "set_var": "firstNode", "target": first_node, "action": "jump", "depth_label": f"firstNode (방 {depth}층)"}
        first_node.next_node.next_node = first_node
        yield {"msg": "역방향 꺾기", "desc": "내 뒤에 있던 놈이 바로 나를 보게 화살표를 확 꺾어버립니다!!", "line": 8, "reconnect": {"src": first_node.next_node, "tgt": first_node}}
        first_node.next_node = None
        yield {"msg": "기존 꼬리 잘라내기", "desc": "이제 내가 맨 끝이므로 불필요한 화살표를 절단합니다 (NULL).", "line": 9, "reconnect": {"src": first_node, "tgt": None}}
        
        self.call_stack.pop()
        yield {"msg": "방 철거", "desc": f"{depth}층 작업 끝. 밑층으로 돌아가봅시다.", "line": -1, "stack_update": True}
        return new_head

    # ========================== 액션 라우터 ==========================
    def process_action(self, action):
        if "msg" in action: self.status_var.set("상태: " + action["msg"])
        if "desc" in action: self.update_description(action["desc"])
        if "line" in action: self.highlight_code(action["line"])
        if "depth_label" in action and "firstNode" in self.variables: self.variables["firstNode"].set_label(action["depth_label"])
        if action.get("stack_update"): self.draw_stack()
        
        if "set_var" in action and action["set_var"] in self.variables:
            target = action["target"]
            ptr = self.variables[action["set_var"]]
            ptr.point_to(target)
            if target and ("action" not in action):
                target.set_color("#FFEB3B")
                self.after(300, lambda t=target: t.set_color("#87CEFA"))
        
        if action.get("action") == "jump" and action.get("target"):
            action["target"].jump_and_highlight()
            
        if "reconnect" in action:
            self.set_next(action["reconnect"]["src"], action["reconnect"]["tgt"])
            
        if "align" in action:
            self.align_list(action["align"]["head"], action["align"]["x"], action["align"]["y"])
            if "align2" in action:
                self.align_list(action["align2"]["head"], action["align2"]["x"], action["align2"]["y"])
                
        if action.get("align2_zipped"):
            # 병합되는 두 리스트를 나란히 예쁘게 그려주는 특별함수
            self.align_list(self.head_node_ptr, 100, 150)
            self.align_list(self.head_node_ptr2, 100, 250)

        if "Q7" in self.current_q and action.get("msg") == "방 철거" and len(self.call_stack) == 0:
            self.after(800, lambda: self.align_list(self.variables["ptrHead"].target_node, 100, 150))
            self.is_playing = False
            self.btn_play.config(text="자동 재생 ▶", bg="#2196F3")
            self.update_description("✅ 리스트가 전부 뒤집혔습니다! 모든 재귀 복귀 성공!")

        self.draw_stack()
        
    def step_forward(self):
        if not self.generator: return
        try: self.process_action(next(self.generator))
        except StopIteration:
            self.generator = None
            self.status_var.set("상태: 알고리즘 완료!")

    def toggle_play(self):
        self.is_playing = not self.is_playing
        if self.is_playing:
            self.btn_play.config(text="일시 정지 ⏸", bg="#FF9800")
            self.auto_step()
        else:
            self.btn_play.config(text="자동 재생 ▶", bg="#2196F3")

    def auto_step(self):
        if self.is_playing and self.generator:
            try:
                self.process_action(next(self.generator))
                self.after(2000, self.auto_step)
            except StopIteration:
                self.generator = None
                self.is_playing = False
                self.btn_play.config(text="자동 재생 ▶", bg="#2196F3")

    def reset_all(self):
        self.is_playing = False
        self.init_data()

    def run_animation_loop(self):
        for n in self.nodes: n.update_position()
        for arr in self.arrows: arr.update_position()
        for v in self.variables.values(): v.update_position()
        self.after(16, self.run_animation_loop)

if __name__ == "__main__":
    app = LinkedListVisualizer()
    app.mainloop()
