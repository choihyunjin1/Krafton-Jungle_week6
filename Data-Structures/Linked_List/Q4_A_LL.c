//////////////////////////////////////////////////////////////////////////////////

/* CE1007/CZ1007 Data Structures
Lab Test: Section A - Linked List Questions
Purpose: Implementing the required functions for Question 4 */

//////////////////////////////////////////////////////////////////////////////////

#include <stdio.h>
#include <stdlib.h>

//////////////////////////////////////////////////////////////////////////////////

typedef struct _listnode
{
	int item;
	struct _listnode *next;
} ListNode;			// You should not change the definition of ListNode

typedef struct _linkedlist
{
	int size;
	ListNode *head;
} LinkedList;			// You should not change the definition of LinkedList


//////////////////////// function prototypes /////////////////////////////////////

// You should not change the prototype of this function
void moveEvenItemsToBack(LinkedList *ll);

void printList(LinkedList *ll);
void removeAllItems(LinkedList *ll);
ListNode * findNode(LinkedList *ll, int index);
int insertNode(LinkedList *ll, int index, int value);
int removeNode(LinkedList *ll, int index);

//////////////////////////// main() //////////////////////////////////////////////

int main()
{
	LinkedList ll;
	int c, i, j;
	c = 1;
	//Initialize the linked list 1 as an empty linked list
	ll.head = NULL;
	ll.size = 0;


	printf("1: Insert an integer to the linked list:\n");
	printf("2: Move all even integers to the back of the linked list:\n");
	printf("0: Quit:\n");

	while (c != 0)
	{
		printf("Please input your choice(1/2/0): ");
		scanf("%d", &c);

		switch (c)
		{
		case 1:
			printf("Input an integer that you want to add to the linked list: ");
			scanf("%d", &i);
			j = insertNode(&ll, ll.size, i);
			printf("The resulting linked list is: ");
			printList(&ll);
			break;
		case 2:
			moveEvenItemsToBack(&ll); // You need to code this function
			printf("The resulting linked list after moving even integers to the back of the linked list is: ");
			printList(&ll);
			removeAllItems(&ll);
			break;
		case 0:
			removeAllItems(&ll);
			break;
		default:
			printf("Choice unknown;\n");
			break;
		}
	}
	return 0;
}

//////////////////////////////////////////////////////////////////////////////////

void moveEvenItemsToBack(LinkedList *ll)
{
	// 리스트가 비어있거나 노드가 1개 이하면 옮길 것도 없으니 바로 종료!
    if (ll == NULL || ll->head == NULL || ll->head->next == NULL)
        return;

    ListNode *cur = ll->head;      // 현재 짝수인지 홀수인지 검사할 녀석
    ListNode *prev = NULL;         // 항상 cur의 바로 앞을 쫓아다니는 녀석 (cur를 떼어낼 때 연결 끊어주기 위해 필요)
    ListNode *tail = ll->head;     // 짝수 발견하면 뒤에 붙여야 하니까 맨 끝 위치를 가리킬 녀석
							       // 

    // 1. 진짜 꼬리(끝 노드) 찾기
    // 리스트 끝까지 쭈욱 돌아서 꼬리가 누군지 파악함
    while (tail->next != NULL)
        tail = tail->next;

    ListNode *oldTail = tail;      // 원래 리스트의 진짜 꼬리를 기억해 둠
                                   // 이걸 안 해두면 나중에 짝수를 뒤로 보냈을 때 다시 또 검사하면서 무한 루프에 빠짐...

    // 2. 본격적인 순회 시작 (단, 원래 리스트의 꼬리(oldTail)까지만 검사!)
    while (cur != NULL && cur != oldTail->next)
    {
        if (cur->item % 2 == 0)  // 오! 들어있는 값이 짝수다! 넌 뒤로 가라
        {
            ListNode *nextNode = cur->next; // 이 짝수를 떼어내면 이어붙일 다음 놈을 미리 기억해 둠

            // 일단 현재 위치에서 짝수 노드 떼어내기
            if (prev == NULL)        // 하필 맨 앞(head) 놈이 짝수였을 경우
                ll->head = nextNode; // 머리를 두 번째 놈으로 바꿔버림 (기존 머리 싹둑)
            else                     // 중간 어딘가에 있는 놈이었을 경우
                prev->next = nextNode; // 앞 놈이랑 뒷 놈을 바로 다이렉트로 연결 (가운데 짝수 싹둑)

            // 떨어져 나온 짝수 노드를 꼬리 뒤에 갖다 붙이기
            tail->next = cur;    // 기존 꼬리가 가리키는 다음 놈을 이 짝수 노드로 설정
            cur->next = NULL;    // 이제 얘가 맨 끝 노드니까 next에는 NULL 줘야 함
            tail = cur;          // 꼬리 위치 포인터를 새로 붙인 노드로 업데이트!

            // 검사할 타겟(cur) 이동
            // 짝수를 뽑아냈으므로, prev는 이동할 필요 없이 cur만 아까 기억해둔 nextNode로 이동시킴
            cur = nextNode;
        }
        else  // 홀수네 넌 그냥 원래 자리에 있어
        {
            prev = cur;          // 짝수가 아니니까 prev도 정상적으로 쫄래쫄래 따라감
            cur = cur->next;     // cur도 다음 놈 검사하러 이동
        }
    }
}

/*
===================================================================
[ moveEvenItemsToBack 시각적 흐름도 ]

예시: 1 -> 2 -> 3 -> 4 (4가 처음 파악한 oldTail)

[초기 상태]
Head -> [1] -> [2] -> [3] -> [4(oldTail)] -> NULL

[Step 1] cur가 1을 가리킴 (홀수)
 -> 변화 없음, 다음 노드로 이동

[Step 2] cur가 2를 가리킴 (짝수)
 -> 2를 떼어내서 현재 꼬리(4) 뒤에 연결!
Head -> [1] -> [3] -> [4(oldTail)] -> [2(new tail)] -> NULL

[Step 3] cur가 3을 가리킴 (홀수)
 -> 변화 없음, 다음 노드로 이동

[Step 4] cur가 4를 가리킴 (짝수이자 oldTail 도달!)
 -> oldTail이었던 4도 떼어내서 현재 꼬리(2) 뒤에 연결!
Head -> [1] -> [3] -> [2] -> [4(new tail)] -> NULL

[최종 결과]  
1 -> 3 -> 2 -> 4 -> NULL (홀수 먼저, 짝수 나중)
===================================================================
*/

///////////////////////////////////////////////////////////////////////////////////

void printList(LinkedList *ll){

	ListNode *cur;
	if (ll == NULL)
		return;
	cur = ll->head;

	if (cur == NULL)
		printf("Empty");
	while (cur != NULL)
	{
		printf("%d ", cur->item);
		cur = cur->next;
	}
	printf("\n");
}


void removeAllItems(LinkedList *ll)
{
	ListNode *cur = ll->head;
	ListNode *tmp;

	while (cur != NULL){
		tmp = cur->next;
		free(cur);
		cur = tmp;
	}
	ll->head = NULL;
	ll->size = 0;
}


ListNode *findNode(LinkedList *ll, int index){

	ListNode *temp;

	if (ll == NULL || index < 0 || index >= ll->size)
		return NULL;

	temp = ll->head;

	if (temp == NULL || index < 0)
		return NULL;

	while (index > 0){
		temp = temp->next;
		if (temp == NULL)
			return NULL;
		index--;
	}

	return temp;
}

int insertNode(LinkedList *ll, int index, int value){

	ListNode *pre, *cur;

	if (ll == NULL || index < 0 || index > ll->size + 1)
		return -1;

	// If empty list or inserting first node, need to update head pointer
	if (ll->head == NULL || index == 0){
		cur = ll->head;
		ll->head = malloc(sizeof(ListNode));
		ll->head->item = value;
		ll->head->next = cur;
		ll->size++;
		return 0;
	}


	// Find the nodes before and at the target position
	// Create a new node and reconnect the links
	if ((pre = findNode(ll, index - 1)) != NULL){
		cur = pre->next;
		pre->next = malloc(sizeof(ListNode));
		pre->next->item = value;
		pre->next->next = cur;
		ll->size++;
		return 0;
	}

	return -1;
}


int removeNode(LinkedList *ll, int index){

	ListNode *pre, *cur;

	// Highest index we can remove is size-1
	if (ll == NULL || index < 0 || index >= ll->size)
		return -1;

	// If removing first node, need to update head pointer
	if (index == 0){
		cur = ll->head->next;
		free(ll->head);
		ll->head = cur;
		ll->size--;

		return 0;
	}

	// Find the nodes before and after the target position
	// Free the target node and reconnect the links
	if ((pre = findNode(ll, index - 1)) != NULL){

		if (pre->next == NULL)
			return -1;

		cur = pre->next;
		pre->next = cur->next;
		free(cur);
		ll->size--;
		return 0;
	}

	return -1;
}
