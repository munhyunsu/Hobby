/** Program to read a single character of different language
using wchar_t array and scanf. The program prints back the
string along with its length
*/

#include <stdio.h>
#include <stdlib.h>
#include <wchar.h>
#include <locale.h>

int main() {

    wchar_t string[100];

    setlocale(LC_ALL, "");

    printf ("Enter a string: ");
    scanf("%ls",string);

    printf("String Entered: %ls: length: %lu", string, wcslen(string));

    return 0;
}
