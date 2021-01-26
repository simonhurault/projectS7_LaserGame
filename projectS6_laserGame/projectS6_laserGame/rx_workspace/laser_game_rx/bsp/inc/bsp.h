/*
 * bsp.h
 *
 *  Created on: 5 août 2017
 *      Author: Laurent
 */

#ifndef BSP_INC_BSP_H_
#define BSP_INC_BSP_H_

#include "stm32f0xx.h"

/*
 * LED driver functions
 */

void	BSP_LED_Init	(void);
void	BSP_LED_On	(void);
void	BSP_LED_Off	(void);
void	BSP_LED_Toggle	(void);


/*
 * Push-Button driver functions
 */

void		BSP_PB_Init		(void);
uint8_t	BSP_PB_GetState	(void);


/*
 * Debug Console init
 */

void	BSP_Console_Init	(void);

/*
 * ADC functions
 */

void BSP_ADC_Init		(void);


/*
 * Timer functions
 */

void BSP_TIMER_Timebase_Init	(void);
void BSP_TIMER_IC_Init		(void);



void BSP_PB13_Init(void);


/*
 * NVIC initialization
 */

void BSP_NVIC_Init				(void);

#endif /* BSP_INC_BSP_H_ */


