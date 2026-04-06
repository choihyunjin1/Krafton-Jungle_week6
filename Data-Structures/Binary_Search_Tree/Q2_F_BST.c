//////////////////////////////////////////////////////////////////////////////////

/* CE1007/CZ1007 Data Structures
Lab Test: Section F - Binary Search Trees Questions
Purpose: Implementing the required functions for Question 2 */

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
void inOrderTraversal(BSTNode *node);

void insertBSTNode(BSTNode **node, int value);

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
	BSTNode *root;
	root = NULL;

	printf("1: Insert an integer into the binary search tree;\n");
	printf("2: Print the in-order traversal of the binary search tree;\n");
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
			printf("The resulting in-order traversal of the binary search tree is: ");
			inOrderTraversal(root); // You need to code this function
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

void inOrderTraversal(BSTNode *root)
{	
	Stack s;
	s.top = NULL; // 스택 초기화 (우리가 지나온 경로를 기억할 가방)

	// 현재 노드가 있거나, 스택에 기억해둔 노드가 아직 모자라게 남아있다면 계속 빙글빙글 돕니다.
	while (root != NULL || !isEmpty(&s))
	{
		if (root != NULL)
		{
			// 일단 왼쪽으로 갈 수 있는 데까지 쭉쭉 내려가면서, 지나온 길을 스택에 푸시!
			push(&s, root);
			root = root->left;
		}
		else
		{
			// 왼쪽 끝까지 도착해서 더 이상 갈 곳이 없게 되면(NULL)?
			// 스택에서 가장 최근에 지나쳐온 노드를 꺼냄(pop)
			root = pop(&s);
			
			// 해당 노드의 값을 출력! 이게 In-order(Left -> Root -> Right)의 핵심!
    		printf("%d ", root->item);
			
			// 왼쪽 자식 처리 다 했고 나 자신(Root)도 출력했으니 이젠 "오른쪽 자식"으로 탐험 시작!
    		root = root->right;
		}
	}
}

/*
===================================================================
[ inOrderTraversal(중위 순회) 시각적 흐름도 ]

예시 트리:
        (5)
       /   \
     (3)   (7)
    /  \
  (1)  (4)

순회 규칙: Left -> Root -> Right (왼쪽 먼저, 그 다음 나, 마지막으로 오른쪽)

[Step 1] 왼쪽 끝까지 파고들기
- 방문: 5 -> 3 -> 1
- 스택: [5, 3, 1]
- root: 1의 왼쪽(NULL) 도달!

[Step 2] 갈 곳 없으니 Pop & Print (1번 노드)
- 스택: [5, 3]
- 출력: 1
- root: 1의 오른쪽(NULL)

[Step 3] 갈 곳 없으니 Pop & Print (3번 노드)
- 스택: [5]
- 출력: 1 3
- root: 3의 오른쪽(4) -> 이제 4로 감!

[Step 4] 4도 왼쪽 끝(NULL) 확인 후 Pop & Print
- 스택: [5, 4] -> [5]
- 출력: 1 3 4
- root: 4의 오른쪽(NULL) 도달

[Step 5] 더 이상 갈 곳 없으니 Pop & Print (5번 노드)
- 스택: []
- 출력: 1 3 4 5
- root: 5의 오른쪽(7) -> 이제 7로 감!

[Step 6] 7 처리
- 스택: [7] -> []
- 출력: 1 3 4 5 7
- root: 7의 오른쪽(NULL) 도달 후 스택도 비었으므로 루프 완전 종료!
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
