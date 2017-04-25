/* Hello World */
#include <linux/module.h>

MODULE_LICENSE("Dual BSD/GPL");

int my_init_module(void) {
    printk("<1>Hello, Hyunsu Mun\n");
    return 0;
}

void my_cleanup_module(void) {
    printk("<1>Goodbye, Hyunsu Mun\n");
}

module_init(my_init_module);
module_exit(my_cleanup_module);
