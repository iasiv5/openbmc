/* SPDX-License-Identifier: GPL-2.0-or-later OR MIT */
/*
 * ASPEED AST2700 Clock Binding Definitions
 */

#ifndef __DT_BINDINGS_CLOCK_AST2700_H
#define __DT_BINDINGS_CLOCK_AST2700_H

/* SCU Clocks */
#define AST2700_CLK_PLLIN     0
#define AST2700_CLK_HPLL      1
#define AST2700_CLK_APLL      2
#define AST2700_CLK_MPLL      3
#define AST2700_CLK_DPLL      4
#define AST2700_CLK_EPLL      5
#define AST2700_CLK_RPLL      6
#define AST2700_CLK_MCU       7
#define AST2700_CLK_AHB       8
#define AST2700_CLK_APB       9
#define AST2700_CLK_UART      10
#define AST2700_CLK_SDIO      11
#define AST2700_CLK_SD        12
#define AST2700_CLK_EMMC      13
#define AST2700_CLK_MAC       14
#define AST2700_CLK_USB       15
#define AST2700_CLK_VIDEO     16
#define AST2700_CLK_BCLK      17
#define AST2700_CLK_REFCLK    18
#define AST2700_CLK_24M       19
#define AST2700_CLK_48M       20
#define AST2700_CLK_PCLK      21
#define AST2700_CLK_RTC       22
#define AST2700_CLK_NUM       23

/* SCU1 Clocks */
#define AST2700_CLK1_MCU      0
#define AST2700_CLK1_AHB      1
#define AST2700_CLK1_APB      2
#define AST2700_CLK1_UART     3
#define AST2700_CLK1_PCLK     4

/* SCU2 Clocks */
#define AST2700_CLK2_MCU      0
#define AST2700_CLK2_AHB      1
#define AST2700_CLK2_APB      2
#define AST2700_CLK2_UART     3
#define AST2700_CLK2_PCLK     4

/* SCU3 Clocks */
#define AST2700_CLK3_MCU      0
#define AST2700_CLK3_AHB      1
#define AST2700_CLK3_APB      2
#define AST2700_CLK3_UART     3
#define AST2700_CLK3_PCLK     4

/* SCU4 Clocks */
#define AST2700_CLK4_MCU      0
#define AST2700_CLK4_AHB      1
#define AST2700_CLK4_APB      2
#define AST2700_CLK4_UART     3
#define AST2700_CLK4_PCLK     4

#endif /* __DT_BINDINGS_CLOCK_AST2700_H */
