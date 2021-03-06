/*
 * bsp.h
 *
 *  Created on: 4 mars 2020
 *      Author: simon.hurault
 */

#ifndef BSP_INC_BSP_H_
#define BSP_INC_BSP_H_

void BSP_TIMER_PWM_Init(void);

void BSP_Console_Init(void);

void BSP_PB_Init(void);
uint8_t BSP_PB_GetState(void);

void BSP_NVIC_Init(void);

#endif /* BSP_INC_BSP_H_ */
