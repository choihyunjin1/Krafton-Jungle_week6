//////////////////////////////////////////////////////////////////////////////////

/* CE1007/CZ1007 Data Structures
Lab Test: Section A - Linked List Questions
Purpose: Implementing the required functions for Question 6 */

//////////////////////////////////////////////////////////////////////////////////

#include <stdio.h>  /* 전처리기 지시문       stdio.h = printf, scanf //  stdlib.h = malloc, free 사용가능하게해줌 */
#include <stdlib.h>

//////////////////////////////////////////////////////////////////////////////////

typedef struct _listnode   /* 구조체 선언    typedef 없으면 매 호출마다 struct _listnode 써야함 */
{
	int item;                              /* 노드에 들어갈 데이터 (값) */
	struct _listnode *next;					/* 다음 노드를 가리키는 포인터 (단방향 연결) */
} ListNode;			// You should not change the definition of ListNode

typedef struct _linkedlist
{
	int size;							/* 노드의 총 개수 */
	ListNode *head;						/* 리스트의 첫 번째 노드를 가리키는 머리부분 */
} LinkedList;			// You should not change the definition of LinkedList


//////////////////////// function prototypes /////////////////////////////////////

// You should not change the prototype of this function
int moveMaxToFront(ListNode **ptrHead);  // 포인터의 포인터(**)를 받는 이유는 헤드 자체의 주소값을 바꿔버릴 수 있게 하기 위함

void printList(LinkedList *ll); 						// 리스트 출력 함수
void removeAllItems(LinkedList *ll); 					// 모든 노드 메모리 해제
ListNode * findNode(LinkedList *ll, int index); 		// index번째 노드 찾기
int insertNode(LinkedList *ll, int index, int value); 	// index 위치에 value 추가
int removeNode(LinkedList *ll, int index); 				// index번째 노드 제거


//////////////////////////// main() //////////////////////////////////////////////

int main()
{
	int c = 1, i, j;   // 그냥 1로 초기화 (c = 1 아래에 있던 걸 위로 올림)

	LinkedList ll;
	//Initialize the linked list 1 as an empty linked list 
	ll.head = NULL;
	ll.size = 0;

	// 리스트 초기화화
	printf("1: Insert an integer to the linked list:\n");
	printf("2: Move the largest stored value to the front of the list:\n");
	printf("0: Quit:\n");

	while (c != 0)
	{
		printf("Please input your choice(1/2/0): ");
		scanf("%d", &c);

		switch (c)
		{
		case 1:                   // ll 리스트에 숫자 추가
			printf("Input an integer that you want to add to the linked list: ");
			scanf("%d", &i);
			j = insertNode(&ll, ll.size, i);  // &ll로 가서 ll.size(맨 뒤)에 i 추가
			printf("The resulting linked list is: ");
			printList(&ll);
			break;
		case 2:                   // 제일 큰 값을 앞으로 빼는 기능 실행
			moveMaxToFront(&(ll.head));  // 포인터의 주소를 넘겨야 하기 때문에 & 사용 (&ll.head)
			printf("The resulting linked list after moving largest stored value to the front of the list is: ");
			printList(&ll);
			removeAllItems(&ll);   // 어째서인지 여기선 한 번 실행하면 다 지우고 끝나길 유도함
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

////////////////////////////////////////////////////////////////////////

int moveMaxToFront(ListNode **ptrHead)
{
	// 리스트가 아예 비어있거나 노드가 1개뿐이면 자리를 옮길 필요가 없으니 바로 종료!
	if (*ptrHead == NULL || (*ptrHead)->next == NULL)
		return 0;

    ListNode *cur = (*ptrHead)->next;  // 두 번째 노드부터 본격적으로 탐색할 예정
	ListNode *prev = *ptrHead;         // prev는 cur의 바로 직전 노드를 항상 쫓아감

	ListNode *maxNode = *ptrHead;      // 현재까지 발견된 가장 큰 값을 가진 노드 (일단 첫 번째 노드라고 가정)
	ListNode *maxPrev = NULL;          // 가장 큰 노드의 "직전 노드"를 기억해둬야 나중에 연결을 끊고 이어붙이기 가능
	
	// 끝까지 훑으면서 가장 큰 값과 그 앞 노드를 찾음
	while (cur != NULL)
	{
		if (cur->item > maxNode->item)  // 지금 본 노드가 기존 최댓값보다 크다면?
		{
			maxNode = cur;              // 최댓값 노드 갱신
			maxPrev = prev;             // 최댓값 앞 노드도 같이 갱신
		}
		prev = cur;                     // 다음 놈 검사하기 위해 쫄래쫄래 따라감
		cur = cur->next;                // 다음 놈으로 전진
	}

	// 만약 제일 큰 놈이 원래 맨 앞에 있던 놈이면 굳이 위치를 바꿀 필요가 없음!
	if (maxPrev == NULL)
    	return 0;

	// 이제 진짜 자리 옮기기 시작 (Max 노드를 파서 맨 앞으로)
	maxPrev->next = maxNode->next;      // 1. Max 앞 노드랑 Max 뒷 노드를 이어버림 (Max 분리!)
	maxNode->next = *ptrHead;           // 2. 떼어낸 Max 노드의 다음을 예전 맨 앞 노드(Head)로 연결
	*ptrHead = maxNode;                 // 3. 리스트의 새로운 머리(Head)를 Max 노드로 지정!

	return 0; // 함수가 int형 반환이라 대충 0 리턴 필수
//////////////////////////////////////////////////////////////////////////////////

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

ListNode * findNode(LinkedList *ll, int index){

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
