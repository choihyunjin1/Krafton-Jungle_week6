
//////////////////////////////////////////////////////////////////////////////////

/* CE1007/CZ1007 Data Structures
Lab Test: Section F - Binary Search Trees Questions
Purpose: Implementing the required functions for Question 1 */

//////////////////////////////////////////////////////////////////////////////////

#include <stdio.h>
#include <stdlib.h>

#define BUFFER_SIZE 1024
///////////////////////////////////////////////////////////////////////////////////

typedef struct _bstnode{
	int item;
	struct _bstnode *left;
	struct _bstnode *right;
} BSTNode;   // You should not change the definition of BSTNode

typedef struct _QueueNode {
	BSTNode *data;
	struct _QueueNode *nextPtr;
}QueueNode; // You should not change the definition of QueueNode


typedef struct _queue
{
	QueueNode *head;
	QueueNode *tail;
}Queue; // You should not change the definition of queue

///////////////////////////////////////////////////////////////////////////////////

// You should not change the prototypes of these functions
void levelOrderTraversal(BSTNode *node);

void insertBSTNode(BSTNode **node, int value);

BSTNode* dequeue(QueueNode **head, QueueNode **tail);
void enqueue(QueueNode **head, QueueNode **tail, BSTNode *node);
int isEmpty(QueueNode *head);
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
	printf("2: Print the level-order traversal of the binary search tree;\n");
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
			printf("The resulting level-order traversal of the binary search tree is: ");
			levelOrderTraversal(root); // You need to code this function
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

void levelOrderTraversal(BSTNode* root)
{	
	// 루트가 비어있으면(NULL) 출력할 게 없으니 바로 종료!
	if( root == NULL)
	{
		return ;
	}
	
	QueueNode *head = NULL; // 줄 서는 곳(Queue)의 맨 앞자리
	QueueNode *tail = NULL; // 줄 서는 곳(Queue)의 맨 뒷자리
	
	// 1. 트리 순회의 시작점인 루트 노드를 먼저 큐(대기열)에 넣음
	enqueue( &head, &tail, root);
	
	// 2. 대기열(Queue)이 텅 빌 때까지 무한 반복!
    while(!isEmpty(head))
	{
		// 맨 앞에 줄 서 있는 노드를 데려옴 (Dequeue)
		BSTNode *temp = dequeue(&head, &tail);
		
		// 데려온 노드의 값을 출력 (방문 완료!)
		printf("%d ", temp->item);
		
		// 만약 방금 데려온 노드한테 왼쪽 자식이 있다면? 대기열 맨 뒤에 세움!
		if (temp->left != NULL)
		{
			enqueue( &head, &tail, temp->left);
		}
		
		// 만약 오른쪽 자식도 있다면? 방금 선 왼쪽 자식 다음에 줄을 세움!
		if (temp->right != NULL)
		{
			enqueue( &head, &tail, temp->right);
		}
	}
}

/*
===================================================================
[ levelOrderTraversal(레벨 순회) 시각적 흐름도 ]

예시 트리:
        (5)
       /   \
     (3)   (7)
    /  \     \
  (1)  (4)   (9)

[초기 상태] 
- 큐: [5(루트)]

[Step 1] dequeue -> 5 출력 | 자식(3, 7) enqueue
- 출력: 5
- 큐: [3, 7]

[Step 2] dequeue -> 3 출력 | 자식(1, 4) enqueue
- 출력: 5 3
- 큐: [7, 1, 4]

[Step 3] dequeue -> 7 출력 | 자식(9) enqueue
- 출력: 5 3 7
- 큐: [1, 4, 9]

[Step 4~6] dequeue -> 1, 4, 9 차례대로 출력 (더 이상 자식이 없으므로 enqueue 안 함)
- 출력: 5 3 7 1 4 9
- 큐: [] (비었으므로 와일문 종료!)

[최종 결과]  
위에서 아래로(Level-by-Level), 왼쪽에서 오른쪽 순서대로 방문 성공!
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

// enqueue node
void enqueue(QueueNode **headPtr, QueueNode **tailPtr, BSTNode *node)
{
	// dynamically allocate memory
	QueueNode *newPtr = malloc(sizeof(QueueNode));

	// if newPtr does not equal NULL
	if (newPtr != NULL) {
		newPtr->data = node;
		newPtr->nextPtr = NULL;

		// if queue is empty, insert at head
		if (isEmpty(*headPtr)) {
			*headPtr = newPtr;
		}
		else { // insert at tail
			(*tailPtr)->nextPtr = newPtr;
		}

		*tailPtr = newPtr;
	}
	else {
		printf("Node not inserted");
	}
}

BSTNode* dequeue(QueueNode **headPtr, QueueNode **tailPtr)
{
	BSTNode *node = (*headPtr)->data;
	QueueNode *tempPtr = *headPtr;
	*headPtr = (*headPtr)->nextPtr;

	if (*headPtr == NULL) {
		*tailPtr = NULL;
	}

	free(tempPtr);

	return node;
}

int isEmpty(QueueNode *head)
{
	return head == NULL;
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
