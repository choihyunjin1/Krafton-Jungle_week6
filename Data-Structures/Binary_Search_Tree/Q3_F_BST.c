//////////////////////////////////////////////////////////////////////////////////

/* CE1007/CZ1007 Data Structures
Lab Test: Section F - Binary Search Trees Questions
Purpose: Implementing the required functions for Question 3 */

//////////////////////////////////////////////////////////////////////////////////

#include <stdio.h>
#include <stdlib.h>

//////////////////////////////////////////////////////////////////////////////////

typedef struct _bstnode{
	int item;
	struct _bstnode *left;
	struct _bstnode *right;
} BSTNode;   // You should not change the definition of BSTNode

typedef struct _stackNode{
	BSTNode *data;
	struct _stackNode *next;
}StackNode; // You should not change the definition of StackNode

typedef struct _stack
{
	StackNode *top;
}Stack; // You should not change the definition of Stack

///////////////////////// function prototypes ////////////////////////////////////

// You should not change the prototypes of these functions
void preOrderIterative(BSTNode *root);

void insertBSTNode(BSTNode **node, int value);

// You may use the following functions or you may write your own
void push(Stack *stack, BSTNode *node);
BSTNode *pop(Stack *s);
BSTNode *peek(Stack *s);
int isEmpty(Stack *s);
void removeAll(BSTNode **node);

///////////////////////////// main() /////////////////////////////////////////////

int main()
{
	int c, i;
	c = 1;

	//Initialize the Binary Search Tree as an empty Binary Search Tree
	BSTNode * root;
	root = NULL;

	printf("1: Insert an integer into the binary search tree;\n");
	printf("2: Print the pre-order traversal of the binary search tree;\n");
	printf("0: Quit;\n");


	while (c != 0)
	{
		printf("Please input your choice(1/2/0): ");
		scanf("%d", &c);

		switch (c)
		{
		case 1:
			printf("Input an integer that you want to insert into the Binary Search Tree: ");
			scanf("%d", &i);
			insertBSTNode(&root, i);
			break;
		case 2:
			printf("The resulting pre-order traversal of the binary search tree is: ");
			preOrderIterative(root); // You need to code this function
			printf("\n");
			break;
		case 0:
			removeAll(&root);
			break;
		default:
			printf("Choice unknown;\n");
			break;
		}

	}

	return 0;
}

//////////////////////////////////////////////////////////////////////////////////

void preOrderIterative(BSTNode *root)
{
    Stack s;
    s.top = NULL; // 스택 초기화 (나중에 다시 돌아와서 '오른쪽'으로 가야 할 곳을 기억하는 용도)

	// 현재 파고드는 노드가 있거나 혹은 스택에 저장해둔 게 있으면 계속 탐색!
    while (root != NULL || !isEmpty(&s))
    {
        if (root != NULL)
        {
			// Pre-order(전위 순회)는 "Root -> Left -> Right" 원칙!
			// 그러니까 노드를 만나자마자 일단 값을 시원하게 출력해버림!
            printf("%d ", root->item);
			
			// 이따가 "오른쪽"으로 가야 한다는 사실을 까먹지 않기 위해 현재 노드를 스택에 킵(Push)해둠
            push(&s, root);
			
			// 그리고 곧바로 왼쪽으로 끝까지 냅다 직진함
            root = root->left;
        }
        else
        {
			// 만약 왼쪽을 타고 내려가다가 길 끝(NULL)을 만났다면?
			// 아까 스택에 킵해뒀던 노드를 하나 꺼내서(Pop)...
            root = pop(&s);
			
			// 그 노드의 "오른쪽" 길로 방향을 틂
            root = root->right;
        }
    }
}

/*
===================================================================
[ preOrderIterative(전위 순회) 시각적 흐름도 ]

예시 트리:
        (5)
       /   \
     (3)   (7)
    /  \      \
  (1)  (4)    (9)

순회 규칙: Root -> Left -> Right (내 거 먼저 출력, 그 다음 왼쪽 쭉, 마지막에 오른쪽)

[Step 1] 내려가면서 일단 다 출력하고 스택에 킵!
- 방문 & 출력: 5 -> 3 -> 1
- 스택: [5, 3, 1]
- 현재 출력된 값: 5 3 1
- root: 1의 왼쪽(NULL)에 도달해서 이제 스택 꺼낼 타이밍!

[Step 2] 갈 길 막힘. Pop 하고 오른쪽으로 틀기
- Pop: 1
- 1의 오른쪽 = NULL -> 다시 else로 들어감

[Step 3] 연속 Pop (다음 오른쪽 길 찾기)
- Pop: 3
- 3의 오른쪽 = 4 -> 이제 4로 방향 전환 완료!

[Step 4] 발견한 오른쪽 길 파고들기
- root(4) != NULL 이니까 다시 if로 진입
- 출력: 5 3 1 4
- 스택에 4 킵 후 왼쪽 확인 (NULL) -> 다시 Pop 해서 오른쪽 확인 (NULL)

[Step 5] 깊은 곳 처리 끝, 뿌리 노드(5) Pop
- Pop: 5
- 5의 오른쪽 = 7 -> 빙고! 7 탐색 시작
- 출력: 5 3 1 4 7
- 7의 오른쪽(9) 타고 가면서 동일하게 진행 -> 무사히 트리 순회 완료!
===================================================================
*/

///////////////////////////////////////////////////////////////////////////////

void insertBSTNode(BSTNode **node, int value){
	if (*node == NULL)
	{
		*node = malloc(sizeof(BSTNode));

		if (*node != NULL) {
			(*node)->item = value;
			(*node)->left = NULL;
			(*node)->right = NULL;
		}
	}
	else
	{
		if (value < (*node)->item)
		{
			insertBSTNode(&((*node)->left), value);
		}
		else if (value >(*node)->item)
		{
			insertBSTNode(&((*node)->right), value);
		}
		else
			return;
	}
}

//////////////////////////////////////////////////////////////////////////////////

void push(Stack *stack, BSTNode * node)
{
	StackNode *temp;

	temp = malloc(sizeof(StackNode));

	if (temp == NULL)
		return;
	temp->data = node;

	if (stack->top == NULL)
	{
		stack->top = temp;
		temp->next = NULL;
	}
	else
	{
		temp->next = stack->top;
		stack->top = temp;
	}
}


BSTNode * pop(Stack * s)
{
	StackNode *temp, *t;
	BSTNode * ptr;
	ptr = NULL;

	t = s->top;
	if (t != NULL)
	{
		temp = t->next;
		ptr = t->data;

		s->top = temp;
		free(t);
		t = NULL;
	}

	return ptr;
}

BSTNode * peek(Stack * s)
{
	StackNode *temp;
	temp = s->top;
	if (temp != NULL)
		return temp->data;
	else
		return NULL;
}

int isEmpty(Stack *s)
{
	if (s->top == NULL)
		return 1;
	else
		return 0;
}


void removeAll(BSTNode **node)
{
	if (*node != NULL)
	{
		removeAll(&((*node)->left));
		removeAll(&((*node)->right));
		free(*node);
		*node = NULL;
	}
}
