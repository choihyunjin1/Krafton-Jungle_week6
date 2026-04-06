
/* CE1007/CZ1007 Data Structures
Lab Test: Section E - Binary Trees Questions
Purpose: Implementing the required functions for Question 1 */

//////////////////////////////////////////////////////////////////////////////////

#include <stdio.h>
#include <stdlib.h>

//////////////////////////////////////////////////////////////////////////////////
typedef struct _btnode{
	int item;
	struct _btnode *left;
	struct _btnode *right;
} BTNode;   // You should not change the definition of BTNode

/////////////////////////////////////////////////////////////////////////////////

typedef struct _stackNode{
    BTNode *btnode;
    struct _stackNode *next;
}StackNode;

typedef struct _stack{
    StackNode *top;
}Stack;

///////////////////////// function prototypes ////////////////////////////////////

// You should not change the prototypes of these functions
int identical(BTNode *tree1, BTNode *tree2);

BTNode* createBTNode(int item);

BTNode* createTree();
void push( Stack *stk, BTNode *node);
BTNode* pop(Stack *stk);

void printTree(BTNode *node);
void removeAll(BTNode **node);

///////////////////////////// main() /////////////////////////////////////////////

/* 메인 함수: 트리 생성 및 구조적 동일성 확인을 위한 사용자 메뉴 제공 */
int main()
{
    int c, s;
    char e;
    BTNode *root1, *root2;

    root1 = NULL;
    root2 = NULL;
    c = 1;

    // 안내 메뉴 출력
    printf("1: Create a binary tree1.\n");
    printf("2: Create a binary tree2.\n");
    printf("3: Check whether two trees are structurally identical.\n");
    printf("0: Quit;\n");

    // 사용자 입력을 기준으로 반복적으로 메뉴 수행 (0 입력 시 종료)
    while(c != 0){
        printf("Please input your choice(1/2/3/0): ");
        if(scanf("%d", &c) > 0)
        {
            switch(c)
            {
            case 1:
                removeAll(&root1);        // 기존 생성됐을 수 있는 tree1 메모리 초기화
                printf("Creating tree1:\n");
                root1 = createTree();     // 사용자 입력 기반 첫번째 이진 트리 생성
                printf("The resulting tree1 is: ");
                printTree(root1);         // 입력된 값 확인을 위한 트리 출력
                printf("\n");
                break;
            case 2:
                removeAll(&root2);        // 기존 생성됐을 수 있는 tree2 메모리 초기화
                printf("Creating tree2:\n");
                root2 = createTree();     // 사용자 입력 기반 두번째 이진 트리 생성
                printf("The resulting tree2 is: ");
                printTree(root2);         // 입력된 값 확인을 위한 트리 출력
                printf("\n");
                break;
            case 3:
                s = identical(root1, root2); // 두 트리가 구조적으로 동일한지 판단
                if(s){
                    printf("Both trees are structurally identical.\n");
                }
                else{
                    printf("Both trees are different.\n");
                }
                removeAll(&root1);        // 확인이 끝나면 메모리 누수를 방지하기 위해 생성했던 양쪽 트리 해기
                removeAll(&root2);
                break;
            case 0:
                removeAll(&root1);        // 0 입력 시 프로그램을 종료하기 전에 트리 메모리 정리
                removeAll(&root2);
                break;
            default:
                printf("Choice unknown;\n"); // 잘못된 숫자 입력 (예: 4 등) 시 경고
                break;
            }
		}
        else
        {
            scanf("%c",&e); // 정수가 아닌 문자 등이 입력되어 오류가 발생할 경우, 해당 문자를 지운 뒤 다시 입력 받기
        }

    }
    return 0; // 프로그램 정상 종료
}

//////////////////////////////////////////////////////////////////////////////////

/* 두 이진 트리가 구조적으로 완전히 같은 형태인지 확인하는 함수 */
int identical(BTNode *tree1, BTNode *tree2)

{
   // 두 노드가 모두 NULL이면 이 부분 트리는 구조적으로 동일하다고 판단
   if (tree1 == NULL && tree2 == NULL)
   {
        return 1;
   }
   // 두 노드 중 하나만 NULL이면 구조가 다르다고 판단
   else if(tree1 == NULL || tree2 == NULL)
   {
        return 0;
   }
   else 
   {
        // 양쪽 노드가 모두 존재하면, 각각의 왼쪽 자식과 오른쪽 자식이 모두 동일한지 재귀적으로 검사
        return identical(tree1->left, tree2->left) && identical(tree1->right, tree2->right);
   }
}
/*
1) t1 == NULL && t2 == NULL 이면 1
2) t1 == NULL || t2 == NULL 이면 0
3) 아니면
   identical(t1->left, t2->left) &&
   identical(t1->right, t2->right)
   */
/////////////////////////////////////////////////////////////////////////////////

/* 주어진 값(item)을 가진 새로운 이진 트리 노드를 동적 할당하여 반환하는 함수 */
BTNode *createBTNode(int item){
    BTNode *newNode = malloc(sizeof(BTNode)); // 새로운 트리 노드를 위한 메모리 동적 할당
    newNode->item = item;                     // 노드에 데이터 값 할당
    newNode->left = NULL;                     // 초기 왼쪽 자식을 NULL로 설정
    newNode->right = NULL;                    // 초기 오른쪽 자식을 NULL로 설정
    return newNode;                           // 생성된 노드의 포인터 반환
}

//////////////////////////////////////////////////////////////////////////////////

/* 사용자 입력을 받아 스택 구조를 이용해 이진 트리를 구성하고 루트 노드를 반환하는 함수 */
BTNode *createTree()
{
    Stack stk;
    BTNode *root, *temp;
    char s;
    int item;

    stk.top = NULL; // 트리를 구성할 빈 스택 초기화
    root = NULL;    // 트리의 루트 노드 초기화

    printf("Input an integer that you want to add to the binary tree. Any Alpha value will be treated as NULL.\n");
    printf("Enter an integer value for the root: ");
    
    // 루트 노드를 입력 받음. 문자가 섞이거나 비정상 입력이면 NULL 처리 로직으로 흐름
    if(scanf("%d",&item) > 0)
    {
        root = createBTNode(item); // 입력받은 값으로 루트 노드 생성
        push(&stk,root);           // 생성한 루트 노드를 자식 처리를 위해 스택에 푸시
    }
    else
    {
        scanf("%c",&s); // 잘못된 입력(문자 등) 소비
    }

    // 스택에서 노드를 순차적으로 꺼내가며(pop) 왼쪽/오른쪽 자식을 입력받음
    while((temp =pop(&stk)) != NULL)
    {
        // 현재 노드(temp)의 왼쪽 자식 값 입력 요구
        printf("Enter an integer value for the Left child of %d: ", temp->item);

        if(scanf("%d",&item)> 0)
        {
            temp->left = createBTNode(item); // 값 입력 시 왼쪽 자식 노드 생성
        }
        else
        {
            scanf("%c",&s); // 문자 입력 시 NULL 처리하고 문자 버퍼 비우기
        }

        // 현재 노드(temp)의 오른쪽 자식 값 입력 요구
        printf("Enter an integer value for the Right child of %d: ", temp->item);
        if(scanf("%d",&item)>0)
        {
            temp->right = createBTNode(item); // 값 입력 시 오른쪽 자식 노드 생성
        }
        else
        {
            scanf("%c",&s); // 문자 입력 시 NULL 처리하고 문자 버퍼 비우기
        }

        // 스택(LIFO) 특성상 나중에 넣은 것이 먼저 꺼내지므로 오른쪽을 먼저 넣고 왼쪽을 나중에 넣음. 즉, 순회 중 왼쪽 자식을 먼저 처리하게 됨.
        if(temp->right != NULL)
            push(&stk,temp->right); // 오른쪽 자식이 있으면 다음 작업 대상이 되도록 스택에 푸시
        if(temp->left != NULL)
            push(&stk,temp->left);  // 왼쪽 자식이 있으면 다음 작업 대상이 되도록 스택에 푸시
    }
    return root; // 완성된 트리의 루트 노드 반환
}

/* 트리 노드의 자식 연결 처리를 위해 스택 맨 위에 노드를 추가(push)하는 함수 */
void push( Stack *stk, BTNode *node){
    StackNode *temp;

    temp = malloc(sizeof(StackNode)); // 스택 노드를 위한 메모리 동적 할당
    if(temp == NULL)
        return; // 할당 실패 시 그대로 반환
    temp->btnode = node; // 푸시할 트리 노드의 주소를 스택 내부 임시 변수에 저장
    
    if(stk->top == NULL){ // 스택이 비어있는 경우
        stk->top = temp;
        temp->next = NULL;
    }
    else{ // 기존 스택에 요소가 있는 경우, 제일 위에 새 노드를 연결
        temp->next = stk->top;
        stk->top = temp;
    }
}

/* 스택의 맨 위에서 노드를 꺼내(pop) 반환하는 함수 */
BTNode* pop(Stack *stk){
   StackNode *temp, *top;
   BTNode *ptr;
   ptr = NULL;

   top = stk->top; // 스택의 맨 위 노드를 top 포인터로 가리킴
   if(top != NULL){
        temp = top->next;     // 다음 노드를 temp에 임시 저장
        ptr = top->btnode;    // 맨 위 노드가 가지고 있던 트리 노드 주소를 ptr에 저장

        stk->top = temp;      // 스택의 맨 위를 다음 노드로 변경 (pop 수행)
        free(top);            // 기존 맨 위 스택 노드 메모리 해제
        top = NULL;
   }
   return ptr; // 꺼낸 트리 노드의 주소를 반환
}

/* 중위 순회(In-order traversal: Left -> Root -> Right) 방식으로 트리를 출력하는 함수 */
void printTree(BTNode *node){
    if(node == NULL) return; // 노드가 비어있으면 함수 종료 (기저 조건)

    printTree(node->left);    // 왼쪽 자식 트리를 재귀적으로 순회
    printf("%d ",node->item); // 현재 노드의 값을 출력
    printTree(node->right);   // 오른쪽 자식 트리를 재귀적으로 순회
}

/* 후위 순회 방식으로 트리의 모든 노드에 할당된 메모리를 안전하게 해제하는 함수 */
void removeAll(BTNode **node){
    if(*node != NULL){
        removeAll(&((*node)->left));  // 왼쪽 자식 트리 메모리 해제 재귀 호출
        removeAll(&((*node)->right)); // 오른쪽 자식 트리 메모리 해제 재귀 호출
        free(*node);                  // 자식들을 모두 비운 후 현재 노드 메모리 해제
        *node = NULL;                 // 해제된 포인터를 NULL로 초기화하여 댕글링 포인터 방지
    }
}
