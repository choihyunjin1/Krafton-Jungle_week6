import tkinter as tk
from tkinter import ttk
import time
import math

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
        # 주인공 강조를 위한 통통 튀는 애니메이션!
        self.set_color("#FF5252") # 눈에 띄는 빨간색으로!
        self.target_y = self.original_y - 40 # 위로 튀어오름
        self.canvas.after(200, lambda: setattr(self, 'target_y', self.original_y + 10)) # 아래로 살짝 파고듦
        self.canvas.after(350, lambda: setattr(self, 'target_y', self.original_y)) # 원상 복구
        self.canvas.after(800, lambda: self.set_color("#87CEFA")) # 색상 복구

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
            self.canvas.itemconfig(self.line, arrow=tk.NONE)
            self.canvas.itemconfig(self.line, dash=(4,4), fill="#999")
        else:
            self.canvas.itemconfig(self.line, arrow=tk.LAST, dash=(), fill="#333")
            ex = self.end_node.x
            ey = self.end_node.y + self.end_node.height / 2
            
            if ex < sx:
                cx1 = sx + 20
                cy1 = sy + 60
                cx2 = ex - 20
                cy2 = ey + 60
                self.canvas.coords(self.line, sx, sy, cx1, cy1, cx2, cy2, ex, ey)
            else:
                self.canvas.coords(self.line, sx, sy, (sx+ex)/2, (sy+ey)/2, ex, ey)

class RecursionVisualizer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("재귀적 연결 리스트 뒤집기 (Recursive Reverse) 애니메이션 시각화")
        self.geometry("1100x750")
        self.configure(bg="#2E2E2E")
        
        self.nodes = []
        self.arrows = []
        self.variables = {}
        
        self.is_playing = False
        self.animation_speed = 50
        
        self.init_ui()
        self.init_data()
        
        self.generator = None
        self.animating = False
        
        self.run_animation_loop()

    def init_ui(self):
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
        main_paned.add(self.canvas, minsize=350)
        
        bottom_paned = tk.PanedWindow(main_paned, orient=tk.HORIZONTAL, bg="#2E2E2E")
        main_paned.add(bottom_paned, minsize=250)
        
        left_panel = tk.Frame(bottom_paned, bg="#1E1E1E")
        bottom_paned.add(left_panel, width=500)
        
        desc_frame = tk.Frame(left_panel, bg="#2C3E50", bd=2, relief=tk.GROOVE)
        desc_frame.pack(fill=tk.X, padx=5, pady=5)
        tk.Label(desc_frame, text="💡 코드 해설 (진행 상황)", font=("맑은 고딕", 10, "bold"), bg="#2C3E50", fg="#F1C40F").pack(anchor=tk.W, padx=5, pady=2)
        
        self.desc_text = tk.Text(desc_frame, height=3, font=("맑은 고딕", 11), bg="#34495E", fg="white", wrap=tk.WORD, bd=0, padx=5, pady=5)
        self.desc_text.pack(fill=tk.X)
        self.desc_text.insert(tk.END, "오른쪽 상단의 [다음 스텝] 또는 [자동 재생] 버튼을 눌러 시각화를 시작하세요.")
        self.desc_text.config(state=tk.DISABLED)

        code_frame = tk.Frame(left_panel, bg="#1E1E1E")
        code_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        tk.Label(code_frame, text="💻 C 소스 코드 (Q7_A_LL.c)", font=("맑은 고딕", 10, "bold"), bg="#1E1E1E", fg="#FFF").pack(anchor=tk.W, pady=2)
        
        self.code_text = tk.Text(code_frame, height=12, font=("Consolas", 11), bg="#282C34", fg="#ABB2BF", wrap=tk.NONE)
        self.code_text.pack(fill=tk.BOTH, expand=True)
        self.code_text.tag_config('highlight', background="#3E4451", foreground="#E5C07B")
        
        c_code = """void RecursiveReverse(ListNode **ptrHead) {
    ListNode *firstNode, *restOfList;
    if (ptrHead == NULL || *ptrHead == NULL)
        return;

    firstNode = *ptrHead;
    restOfList = firstNode->next;

    if (restOfList == NULL)
        return;

    RecursiveReverse(&restOfList);
    
    firstNode->next->next = firstNode;
    firstNode->next = NULL;
    *ptrHead = restOfList;
}"""
        self.code_text.insert(tk.END, c_code)
        self.code_text.config(state=tk.DISABLED)
        
        stack_frame = tk.Frame(bottom_paned, bg="#1E1E1E")
        bottom_paned.add(stack_frame)
        
        tk.Label(stack_frame, text="📚 콜 스택 (Call Stack)", font=("맑은 고딕", 10, "bold"), bg="#1E1E1E", fg="#FFF").pack(anchor=tk.W, padx=5, pady=5)
        self.stack_canvas = tk.Canvas(stack_frame, bg="#282C34", highlightthickness=0)
        self.stack_canvas.pack(fill=tk.BOTH, expand=True)
        
        self.call_stack = []

    def init_data(self):
        self.canvas.delete("all")
        self.stack_canvas.delete("all")
        self.nodes = []
        self.arrows = []
        self.call_stack = []
        
        start_x = 100
        start_y = 150
        values = [10, 20, 30, 40, 50]
        
        for i, v in enumerate(values):
            node = VisualNode(self.canvas, id=i, val=v, x=start_x + i*120, y=start_y)
            self.nodes.append(node)
            
        for i in range(len(self.nodes) - 1):
            self.nodes[i].next_node = self.nodes[i+1]
            arrow = CurvedArrow(self.canvas, self.nodes[i], self.nodes[i+1])
            self.arrows.append(arrow)
            
        last_arrow = CurvedArrow(self.canvas, self.nodes[-1], None)
        self.arrows.append(last_arrow)
        
        self.variables = {
            "ptrHead": VariablePointer(self.canvas, "ptrHead", 50, 50, "#E91E63"),
            "firstNode": VariablePointer(self.canvas, "first", 50, 50, "#FF9800"),
            "restOfList": VariablePointer(self.canvas, "rest", 50, 50, "#4CAF50")
        }
        
        self.variables["ptrHead"].point_to(self.nodes[0], offset_y=-60)
        self.variables["firstNode"].point_to(None)
        self.variables["restOfList"].point_to(None)
        self.variables["firstNode"].set_label("firstNode") # 라벨 리셋
        
        self.highlight_code(-1)
        self.update_description("애니메이션 시작을 대기 중입니다. 기본 노드 5개가 준비되어 있습니다.")
        self.generator = self.algo_generator(1, self.nodes[0]) # 깊이 1부터 시작
        self.status_var.set("상태: 초기화 완료")
        self.is_playing = False
        self.btn_play.config(text="자동 재생 ▶", bg="#2196F3")

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
        for i, frame in enumerate(self.call_stack):
            color = "#FFEB3B" if i == len(self.call_stack)-1 else "#E0E0E0"
            self.stack_canvas.create_rectangle(10, y, 220, y+35, fill="#37474F", outline=color, width=2)
            node_val = frame['head'].val if frame['head'] else "NULL"
            depth = frame['depth']
            self.stack_canvas.create_text(115, y+17, text=f"[스택 {depth}층] Reverse({node_val})", fill="white", font=("Consolas", 10, "bold"))
            y += 45

    def algo_generator(self, depth, current_head):
        self.call_stack.append({'head': current_head, 'depth': depth})
        
        yield {
            "msg": f"RecursiveReverse({current_head.val if current_head else 'NULL'}) 진입",
            "desc": f"🏰 [스택 {depth}층 입장!] 함수가 호출되어 새로운 마술 상자 방이 만들어졌습니다. 이번 방의 타겟 머리는 {current_head.val if current_head else '없음(NULL)'} 입니다.",
            "line": 0, "stack_update": True, 
            "depth_label": f"firstNode (스택 {depth}층)"
        }
        
        yield {"msg": "종료 조건 (Base Case) 검사 중", "desc": "[확인] 빈 리스트가 넘어오지는 않았는지 확인합니다.", "line": 2}
        if current_head is None:
            yield {"msg": "조건 참 -> return", "desc": "아무것도 존재하지 않아 작업 없이 그대로 함수를 종료하고 되돌아갑니다.", "line": 3}
            self.call_stack.pop()
            yield {"msg": "리턴(스택 제거)", "desc": f"스택 {depth}층 붕괴. 되돌아갑니다.", "line": -1, "stack_update": True}
            return current_head
            
        yield {
            "msg": f"firstNode (방 {depth}) 에 대상 기억", 
            "desc": f"[주인공 지정] 이 스택 {depth}층 방의 주인공 'firstNode(주황색)'는 바로 {current_head.val} 입니다. 기억해 두세요!",
            "line": 5, "set_var": "firstNode", "target": current_head,
            "depth_label": f"firstNode (스택 {depth}층)"
        }
        first_node = current_head
        
        yield {
            "msg": "restOfList 분리", 
            "desc": "[변수 분리] 첫 번째 노드 바로 다음에 붙어 있는 나머지 녀석들을 몽땅 'restOfList(초록색)' 로 구별합니다.",
            "line": 6, "set_var": "restOfList", "target": first_node.next_node
        }
        rest_of_list = first_node.next_node
        
        yield {"msg": "거북이 검사", "desc": "[확인] 만약에 분리해 낸 '나머지 리스트'가 아무것도 없다면?", "line": 8}
        
        if rest_of_list is None:
            yield {
                "msg": "단일 노드 반환", 
                "desc": "노드가 1개면 자기 자신이 끝이네요. 더 깊이 들어갈 필요 없이 현재 노드를 통째로 넘기며 귀환합니다.", 
                "line": 9
            }
            yield {"msg": "*ptrHead 유지", "desc": "ptrHead 위치는 변함이 없습니다.", "line": 15, "set_var": "ptrHead", "target": first_node}
            self.call_stack.pop()
            yield {"msg": "리턴(스택 제거)", "desc": "스택 프레임 종료 및 귀환.", "line": -1, "stack_update": True}
            return first_node
            
        yield {
            "msg": f"재귀 호출 (스택 {depth+1}층으로)", 
            "desc": f"🚀 [재귀 다이브러운 돌진!!] \"내 일은 끝났다! 나머지({rest_of_list.val}부터 끝까지)는 알아서 {depth+1}층 방 니가 뒤집어 와!!\" 하며 던집니다.",
            "line": 11
        }
        
        sub_gen = self.algo_generator(depth + 1, rest_of_list)
        new_head = None
        try:
            while True:
                op = next(sub_gen)
                yield op
        except StopIteration as e:
            new_head = e.value
            
        # 여기가 스택 복귀 시 강조 애니메이션 부분!
        yield {
            "msg": f"스택 {depth}층으로 복귀 및 주인공 기상!", 
            "desc": f"🔥 [방 {depth}층으로 스택 팝!] 위층에서 꼬리들을 다 뒤집고 돌아왔습니다! 이 방의 당당한 주인공이었던 firstNode({first_node.val})가 깨어납니다!",
            "line": 11, "set_var": "firstNode", "target": first_node, "set_var2": "restOfList", "target2": rest_of_list,
            "action": "jump", "depth_label": f"firstNode (방 {depth}층)"
        }
        
        yield {
            "msg": "포인터 역회전", 
            "desc": "[진짜 뒤집기!] 내 바로 등 뒤에 있던 녀석(next)이 나(firstNode)를 노려보도록 화살표를 콱! 꺾어버립니다!",
            "line": 13, "anim": "curve_arrow", "source": first_node.next_node, "target": first_node
        }
        first_node.next_node.next_node = first_node
        
        yield {
            "msg": "기존 포인터 절단", 
            "desc": "[꼬리 자르기] 이제 내가 맨 끝이므로 내 뒤통수에 붙어있던 화살표를 쓸모없으니 잘라버립니다 (NULL).",
            "line": 14, "anim": "null_arrow", "source": first_node
        }
        first_node.next_node = None
        
        yield {
            "msg": "완성된 새 머리 반환", 
            "desc": "이 방에서의 일이 완료되었습니다! 새롭게 뒤집어져 반환받았던 머리 노드를 전달체(ptrHead)에 넘깁니다.",
            "line": 15, "set_var": "ptrHead", "target": new_head
        }
        
        self.call_stack.pop()
        yield {"msg": f"스택 {depth}층 종료", "desc": f"✨ [탈출] {depth}층 방의 임무를 무사히 마쳤습니다. 또 다시 한 층 밑으로 결과를 들고 복귀합니다.", "line": -1, "stack_update": True}
        
        return new_head

    def process_action(self, action):
        if "msg" in action:
            self.status_var.set("상태: " + action["msg"])
            
        if "desc" in action:
            self.update_description(action["desc"])
            
        if "line" in action:
            self.highlight_code(action["line"])
            
        if "depth_label" in action:
            self.variables["firstNode"].set_label(action["depth_label"])
            
        if action.get("stack_update"):
            self.draw_stack()
            
        if "set_var" in action:
            var_name = action["set_var"]
            target = action["target"]
            if var_name in self.variables:
                self.variables[var_name].point_to(target)
                if target and "action" not in action:  # jump가 덮어씌워지지 않게
                    target.set_color("#FFEB3B") # 순간 반짝임
                    self.after(300, lambda t=target: t.set_color("#87CEFA"))
                
        if "set_var2" in action:
            var_name = action["set_var2"]
            target = action["target2"]
            if var_name in self.variables:
                self.variables[var_name].point_to(target)

        # 액션: 주인공 노드 통통 튀면서 빨갛게 변하기
        if action.get("action") == "jump":
            target = action["target"]
            if target:
                target.jump_and_highlight()

        if action.get("anim") == "curve_arrow":
            src = action["source"]
            tgt = action["target"]
            for arr in self.arrows:
                if arr.start_node == src:
                    arr.end_node = tgt
                    break

        if action.get("anim") == "null_arrow":
            src = action["source"]
            for arr in self.arrows:
                if arr.start_node == src:
                    arr.end_node = None
                    break
        
        if action.get("msg") == "스택 1층 종료" and len(self.call_stack) == 0:
            self.status_var.set("상태: 알고리즘 완료!")
            self.update_description("✅ 모든 스택 프레임이 정리되며 연결 리스트가 완벽하게 역전되었습니다! 각 스택 층마다 다른 firstNode가 깨어나는 것을 확인하셨나요?")
            self.is_playing = False
            self.btn_play.config(text="자동 재생 ▶", bg="#2196F3")
            self.after(800, self.align_nodes_visually)

    def align_nodes_visually(self):
        curr = self.variables["ptrHead"].target_node
        idx = 0
        while curr:
            curr.target_x = 100 + idx * 120
            curr.target_y = 150
            curr = curr.next_node
            idx += 1

    def step_forward(self):
        if self.generator is None:
            return
            
        try:
            action = next(self.generator)
            self.process_action(action)
        except StopIteration:
            self.generator = None
            self.status_var.set("상태: 작업 완료.")

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
                action = next(self.generator)
                self.process_action(action)
                self.after(2000, self.auto_step) # 애니메이션 감상을 위해 2초로 여유 있게
            except StopIteration:
                self.generator = None
                self.is_playing = False
                self.btn_play.config(text="자동 재생 ▶", bg="#2196F3")

    def reset_all(self):
        self.is_playing = False
        self.init_data()

    def run_animation_loop(self):
        for node in self.nodes:
            node.update_position()
            
        for arrow in self.arrows:
            arrow.update_position()
            
        for var in self.variables.values():
            var.update_position()
            
        self.after(16, self.run_animation_loop)

if __name__ == "__main__":
    app = RecursionVisualizer()
    app.mainloop()
