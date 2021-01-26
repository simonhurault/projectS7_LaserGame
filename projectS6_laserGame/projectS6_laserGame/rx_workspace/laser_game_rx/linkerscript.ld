/*
 * linkerscript.ld
 */

/* Specify the memory areas */
MEMORY
{
	RAM   (xrw)     : ORIGIN = 0x20000000,  LENGTH = 16K
	FLASH (rx)      : ORIGIN = 0x08000000,  LENGTH = 128K
}

/* Specify sections */
SECTIONS
{
    .isr_vectors : 
    { 
    	*(.isr_vector)	/* Interrupts vector table */
    } >FLASH

    .text :
    {
        *(.text)      	/* Program code */
        *(.rodata)    	/* Read only data */
    } >FLASH
      
    .data :
    {
        *(.data)      	/* Initialized data memory */
    } >RAM AT> FLASH

    .bss :
    {
        *(.bss)       	/* Uninitialized data memory */
    } >RAM
}