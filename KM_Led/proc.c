
#include <linux/init.h>
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/fs.h>
#include <asm/uaccess.h>
#include <linux/slab.h>
#include <linux/proc_fs.h> /* proc */
#include <linux/seq_file.h> /* seq_print */
#include <linux/slab.h> /* kmalloc */
#include <linux/cdev.h> /* cdev */
#include <linux/uaccess.h> /* copy to/from user */

MODULE_LICENSE("GPL");

#define RAW_DATA "my_led0"
#define LED_DATA "my_led1"

int led_major = 0;
int led_minor = 0;
unsigned char led0[16];
static char *led1 = NULL;
static struct cdev led1_cdev;
static struct semaphore led1_sem;

#define  BUFF_SIZE      1024
#define  MAJOR_NUMBER   250
static char *buffer  = NULL;
static int   sz_data = 0;

static int my_open( struct inode *inode, struct file *filp ) 
{
  printk( "[VB] openedn" );
  return 0;
}

static int my_release( struct inode *inode, struct file *filp )
{
  printk( "[VB] releasedn" );
  return 0;
}

static ssize_t my_write( struct file *filp, const char *buf, size_t count, loff_t *f_pos )
{
   printk( "[VB] write to buffern %i%b", buf[1], buf[0]);

   if (BUFF_SIZE < count)  sz_data  = BUFF_SIZE;
                           sz_data  = count;

   strncpy( buffer, buf, sz_data);
   led1[buf[1]] = buf[0];
   return count;
}

static ssize_t my_read( struct file *filp, char *buf, size_t count, loff_t *f_pos )
{
  printk( "[VB] read from buffern" );
  copy_to_user( buf, buffer, sz_data);

  return sz_data;
}

static struct file_operations vd_fops = {
  .read = my_read,
  .write = my_write,
  .open = my_open,
  .release = my_release
};



static int led0_proc_read(struct seq_file *s, void *v)
{
    int i = 0;
    for(i = 0; i < 16; i++)
    {
        seq_printf(s, "%c", led0[i]);
    }
    return 0;
}

static int led0_proc_open(struct inode *inode, struct file *file)
{
    return single_open(file, led0_proc_read, NULL);
}

static struct file_operations led0_proc_ops = {
    .owner = THIS_MODULE,
    .open = led0_proc_open,
    .read = seq_read,
    .llseek = seq_lseek,
    .release = single_release
};



static void *led1_seq_start(struct seq_file *s, loff_t *pos)
{
    static unsigned long counter = 0;
    if( *pos == 0 )
    {
        //sema_init(&led1_sem, 1);
        return &counter;
    } else {
        return NULL;
    }
}

static void *led1_seq_next(struct seq_file *s, void *v, loff_t *pos)
{
    /* hmm. */
    return NULL;
}

static void led1_seq_stop(struct seq_file *s, void *v)
{
    /* hmm. */
}

static int led_digit(unsigned char led)
{
    switch(led){
        case 0b01111110:
            return 0;
            break;
        case 0b00110000:
            return 1;
            break;
        case 0b01101101:
            return 2;
            break;
        case 0b01111001:
            return 3;
            break;
        case 0b00110011:
            return 4;
            break;
        case 0b01011011:
            return 5;
            break;
        case 0b00011111:
            return 6;
            break;
        case 0b01110000:
            return 7;
            break;
        case 0b01111111:
            return 8;
            break;
        case 0b01110011:
            return 9;
            break;
        default:
            break;
    }
}

static int led1_seq_show(struct seq_file *s, void *v)
{
    int i = 0;
    if(down_interruptible(&led1_sem))
    {
        return -ERESTARTSYS;
    }
    for(i = 0; i < 16; i++)
    {
        //seq_printf(s, "%c", led1[i]);
        seq_printf(s, "%i", led_digit(led1[i]));
    }
    up(&led1_sem);
    return 0;
}

static struct seq_operations led1_seq_ops = {
    .start = led1_seq_start,
    .next = led1_seq_next,
    .stop = led1_seq_stop,
    .show = led1_seq_show
};

static int led1_proc_open(struct inode *inode, struct file *file)
{
    return seq_open(file, &led1_seq_ops);
}

static struct file_operations led1_proc_ops = {
    .owner = THIS_MODULE,
    .open = led1_proc_open,
    .read = seq_read,
    .llseek = seq_lseek,
    .release = seq_release
};




static int led1_open(struct inode *inode, struct file *filp)
{
    printk(KERN_INFO "led1_open\n");
    return 0;
}

static int led1_release(struct inode *inode, struct file *filp)
{
    printk(KERN_INFO "led1_release\n");
    return 0;
}

static ssize_t led1_write(struct file *filp, const char *buf, size_t count, loff_t *f_pos)
{
    printk(KERN_INFO "led1_write\n");
    int csize = count;
//    if(down_interruptible(&led1_sem))
//    {
//        return -ERESTARTSYS;
//    }
    if(count > 16)
    {
        csize = 16;
    }
    else
    {
        csize = count;
    }
    strncpy(led1, buf, csize);
    //copy_from_user(led1, buf, csize);
//    up(&led1_sem);
    return count;
}

static ssize_t led1_read(struct file *filp, char *buf, size_t count, loff_t *f_pos)
{
    printk(KERN_INFO "led1_read\n");
//    if(down_interruptible(&led1_sem))
//    {
//        return -ERESTARTSYS;
//    }
    char *temp = "wow";
    copy_to_user(buf, temp, 3);
//    up(&led1_sem);
    return 3;
}

static struct file_operations led1_fops = {
    .owner = THIS_MODULE,
    .read = led1_read,
    .write = led1_write,
    .open = led1_open,
    .release = led1_release
};



static int init_led(void)
{
    //int return_value = 0;
    dev_t dev;
    int result;
    
    sema_init(&led1_sem, 1);

    printk(KERN_INFO "Start led\n");

    proc_create_data(RAW_DATA,
            0, /* default mode */
            NULL, /* parent dir */
            &led0_proc_ops,
            NULL /* client data */);
    printk(KERN_INFO "Create led0 success\n");

/*    if(led_major)
    {
        dev = MKDEV(led_major, led_minor);
        result = register_chrdev_region(dev, 1, "my_device");
    }
    else
    {
        result = alloc_chrdev_region(&dev, led_minor, 1,
                        "my_device");
        led_major = MAJOR(dev);
    }
    if(result < 0)
    {
        printk(KERN_WARNING "led: can't get major %d\n", led_major);
        return result;
    }

    printk(KERN_INFO "LED: %d\n", dev);
*/
    register_chrdev(245, "vm_led", &led1_fops);

    led1 = (char*) kmalloc(16, GFP_KERNEL);
    memset(led1, 0, 16);

    //cdev_init(&led1_cdev, &led1_fops);

    proc_create(LED_DATA,
            0, /* default mode */
            NULL, /* parent dir */
            &led1_proc_ops);
    printk(KERN_INFO "Create led1 success\n");


  register_chrdev( 240, "virtual_buffer", &vd_fops );
  buffer = (char*) kmalloc( BUFF_SIZE, GFP_KERNEL );
  memset( buffer, 0, BUFF_SIZE);

  printk( "[VB] initializedn");

    return 0;
}

static void cleanup_led(void)
{
    up(&led1_sem);
    remove_proc_entry(RAW_DATA,
            NULL /* parent dir */);
    printk(KERN_INFO "Remove led0 success\n");
    remove_proc_entry(LED_DATA,
            NULL /* parent dir */);
    printk(KERN_INFO "Remove led1 success\n");
    printk(KERN_INFO "End led\n");
    unregister_chrdev(245, "vm_led");
    kfree(led1);
  unregister_chrdev( 240, "virtual_buffer" );
  kfree( buffer );
  printk( "[VB] exitedn"); 
   //cdev_del(&led1_cdev);
}

module_init(init_led);
module_exit(cleanup_led);
