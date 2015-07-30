#include <stdio.h>

/*
 * '0'在 ascii 表中是第48个，'1'是第49个……以此类推到'9'是第57个。int i='0' 也就是 int i=48；同理 char c=48 也就是 char c='0'。
 * 所以，int a=ch-'0'; 也就是 int a=ch-48; 也就是把 char 转成了 int。
 *
 * For example,
 * 	char ch='9'; 	//也就是ch=57
 * 	int a=ch-'0'; 	//也就是a=57-48=9，这样就是把 char 转成 int 了
 **/

int main(int argc, char *argv[])
{
	char ch = '1';
	unsigned int num = ch - '0';
	printf("num = %d\n", num);
}
