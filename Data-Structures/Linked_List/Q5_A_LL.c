//////////////////////////////////////////////////////////////////////////////////

/* CE1007/CZ1007 Data Structures
Lab Test: Section A - Linked List Questions
Purpose: Implementing the required functions for Question 5 */

//////////////////////////////////////////////////////////////////////////////////

#include <stdio.h>  /* 전처리기 지시문       stdio.h = printf, scanf //  stdlib.h = malloc, free 사용하가능하게해줌     */
#include <stdlib.h>

//////////////////////////////////////////////////////////////////////////////////

typedef struct _listnode   /* 구조체 선언    typedef 없으면 매 호출마다  struct _listnode 이렇게 호출해야함   현재 ListNode 호출되게 하였음                     */
{
	int item;                              /*구조체란  타입이 다른 데이터를 하나로 묶는 방법 */
	struct _listnode *next;					/* 옆 코드로 노드와 노드 연결 ( 단방향임) 다음 구조체의 주소를 가지고있음 */
} ListNode;			// You should not change the definition of ListNode

typedef struct _linkedlist
{
	int size;							/* 노드의 갯수  노드의 시작과 끝을 알려주기 위해 있는 구조체*/
	ListNode *head;
} LinkedList;			// You should not change the definition of LinkedList


///////////////////////// function prototypes ////////////////////////////////////

// You should not change the prototype of this function
void frontBackSplitLinkedList(LinkedList* ll, LinkedList *resultFrontList, LinkedList *resultBackList);

void printList(LinkedList *ll); 						// 리스트를 화면에 보여주는 함수
void removeAllItems(LinkedList *l); 					// 연결리스트의 모든 노드를 메모리에서 해제
ListNode * findNode(LinkedList *ll, int index); 			// index번째 노드의 주소를 찾아서 돌려주는 함수
int insertNode(LinkedList *ll, int index, int value); 	// index 위치에 value를 넣는 함수
int removeNode(LinkedList *ll, int index); 				// index번째 노드 제거


///////////////////////////// main() /////////////////////////////////////////////

int main()
{
	int c = -1, i;
	LinkedList ll;
	LinkedList resultFrontList, resultBackList;

	//Initialize the linked list as an empty linked list
	ll.head = NULL;
	ll.size = 0;

	//Initialize the front linked list as an empty linked list
	resultFrontList.head = NULL;
	resultFrontList.size = 0;

	// Initialize the back linked list as an empty linked list
	resultBackList.head = NULL;
	resultBackList.size = 0;

	printf("1: Insert an integer to the linked list:\n");
	printf("2: Split the linked list into two linked lists, frontList and backList:\n");
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
			insertNode(&ll, ll.size, i);
			printf("The resulting linked list is: ");
			printList(&ll);
			break;
		case 2:
			printf("The resulting linked lists after splitting the given linked list are:\n");
			frontBackSplitLinkedList(&ll, &resultFrontList, &resultBackList); // You need to code this function
			printf("Front linked list: ");
			printList(&resultFrontList);
			printf("Back linked list: ");
			printList(&resultBackList);
			printf("\n");
			removeAllItems(&ll);
			removeAllItems(&resultFrontList);
			removeAllItems(&resultBackList);
			break;
		case 0:
			removeAllItems(&ll);
			removeAllItems(&resultFrontList);
			removeAllItems(&resultBackList);
			break;
		default:
			printf("Choice unknown;\n");
			break;
		}
	}

	return 0;
}

//////////////////////////////////////////////////////////////////////////////////

void frontBackSplitLinkedList(LinkedList *ll, LinkedList *resultFrontList, LinkedList *resultBackList)
{
    ListNode *cur = ll->head;              // 원본 리스트를 순회할 포인터
    int frontSize = (ll->size + 1) / 2;    // 앞쪽 리스트가 가져야 할 노드 개수 계산 (홀수일 경우 앞쪽이 하나 더 가짐)
    
    int i = 0;                             // 현재 순회 중인 노드의 인덱스를 추적할 변수

    while (cur != NULL)                    // 리스트의 끝까지 순회
    {
        if (i < frontSize)                 // 절반 이전의 노드라면
        {
            // 앞쪽 리스트의 끝(resultFrontList->size)에 현재 노드의 값을 삽입
            insertNode(resultFrontList, resultFrontList->size, cur->item);
        }
        else                               // 절반 이후의 노드라면
        {
            // 뒤쪽 리스트의 끝(resultBackList->size)에 현재 노드의 값을 삽입
            insertNode(resultBackList, resultBackList->size, cur->item);
        }

        cur = cur->next;                   // 다음 노드로 이동
        i++;                               // 인덱스 1 증가
    }
}

///////////////////////////////////////////////////////////////////////////////////

void printList(LinkedList *ll){

	ListNode *cur;   // 현재 출력 중인 노드를 가리킬 포인터

	if (ll == NULL)
		return;       // 리스트 자체가 없으면 함수 종료
	cur = ll->head;  // 첫 노드부터 시작
	if (cur == NULL)
		printf("Empty");   // head가 NULL이면 빈 리스트
	while (cur != NULL)
	{
		printf("%d ", cur->item);   // 현재 노드의 값 출력
		cur = cur->next;            // 다음 노드로 이동
	}
	printf("\n");   // 출력 끝나면 줄바꿈
}


void removeAllItems(LinkedList *ll)
{
	ListNode *cur = ll->head;   // 현재 삭제할 노드, 처음엔 첫 노드
	ListNode *tmp;              // 다음 노드를 잠깐 저장할 임시 포인터

	while (cur != NULL){
		tmp = cur->next;   // 현재 노드를 free 하기 전에 다음 노드 주소 백업
		free(cur);         // 현재 노드 메모리 해제
		cur = tmp;         // 다음 노드로 이동
	}
	ll->head = NULL;      // 모든 노드를 지웠으니 head는 NULL
	ll->size = 0;         // 크기도 0으로 초기화
}


ListNode * findNode(LinkedList *ll, int index){

	ListNode *temp;   // 찾으러 이동할 임시 포인터

	if (ll == NULL || index < 0 || index >= ll->size)
		return NULL;   // 리스트가 없거나, index 범위가 잘못되면 실패

	temp = ll->head;  // 일단 첫 노드부터 시작

	if (temp == NULL || index < 0)
		return NULL;   // head가 비어 있으면 찾을 노드가 없음

	while (index > 0){
		temp = temp->next;   // 한 칸 다음 노드로 이동
		if (temp == NULL)
			return NULL;     // 중간에 NULL이면 찾기 실패
		index--;             // 목표 index까지 남은 칸 수 1 감소
	}

	return temp;   // index번째 노드 주소 반환
}

int insertNode(LinkedList *ll, int index, int value){
    // 인덱스 위치에 벨류 삽입
	ListNode *pre, *cur;

	if (ll == NULL || index < 0 || index > ll->size + 1)
		return -1;

	// If empty list or inserting first node, need to update head pointer
	if (ll->head == NULL || index == 0){   // 맨 앞 삽인인가? 판단 맞으면 해드 해제 후 새 리스트를 해드로 가르키게 하고 재연결
		cur = ll->head;                    // 원래 해드 주소를 백업
		ll->head = malloc(sizeof(ListNode)); // 해드에 새 매모리 할당
		ll->head->item = value;              // 넣을려 했던 밸류 맨앞에 삽입
		ll->head->next = cur;                // 해드가 가르키는 노드의 넥스트 노드가 원래 핸드를 가르 키게 함 ( 이로 서 연결됨)
		ll->size++;                          // 노드 늘었으니 size 증가
		return 0;
	}

	// Find the nodes before and at the target position
	// Create a new node and reconnect the links
	if ((pre = findNode(ll, index - 1)) != NULL){
		cur = pre->next;                     // 원래 그 자리에 있던 노드 백업  ( 이걸 하기위 해 findNode로 전 인덱스 노드를 찾음)
		pre->next = malloc(sizeof(ListNode)); // ( 위 와 동일)
		pre->next->item = value;
		pre->next->next = cur;
		ll->size++;
		return 0;
	}

	return -1;
}


int removeNode(LinkedList *ll, int index){

	ListNode *pre, *cur;  

	// 삭제 가능한 최대 index는 size-1
	if (ll == NULL || index < 0 || index >= ll->size)
		return -1;   // 리스트가 없거나 index 범위가 잘못되면 실패

	// 맨 앞 노드(index 0)를 삭제하는 경우
	if (index == 0){
		cur = ll->head->next;   // 두 번째 노드를 미리 백업
		free(ll->head);         // 원래 첫 노드 메모리 해제
		ll->head = cur;         // head를 두 번째 노드로 이동
		ll->size--;             // 크기 1 감소

		return 0;               // 성공
	}

	// 삭제하려는 위치의 앞 노드를 찾는다
	if ((pre = findNode(ll, index - 1)) != NULL){

		if (pre->next == NULL)
			return -1;          // 삭제할 노드가 없으면 실패

		cur = pre->next;        // 실제 삭제할 노드 저장
		pre->next = cur->next;  // 삭제할 노드를 건너뛰도록 연결 변경
		free(cur);              // 삭제 노드 메모리 해제
		ll->size--;             // 크기 1 감소
		return 0;               // 성공
	}

	return -1;                  // 그 외 실패
}
