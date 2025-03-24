#include "board.h"
#include "stm32wlxx_hal.h"
#include "udrv_gpio.h"
#include "variant.h"

extern uint8_t switchATModeFlag ;
uint8_t currentATMode = LORA_AT_MODE;
uint8_t currentEspPowerMode = POWER_ON;



int8_t setCurrentATMode(uint8_t mode) {
    if (mode == LORA_AT_MODE || mode == ESP_AT_MODE) {
        currentATMode = mode; // Set the mode if valid
        switchATModeFlag = 1;
        return 0;             // Success
    } else {
        return -1;             // Failure (invalid mode)
    }
}

// Function to get the current AT mode
uint8_t getCurrentATMode(void) {
    return currentATMode; // Return the current AT mode
}


int8_t setEspPowerMode(uint8_t mode) {
    if (mode == POWER_OFF || mode == POWER_ON) {
        currentEspPowerMode = mode; // Set the power mode if valid
        udrv_gpio_set_dir(PA0, GPIO_DIR_OUT);

        if(mode == POWER_ON)
        {
            udrv_gpio_set_logic(PA0, GPIO_LOGIC_HIGH);
        } else
        {
            udrv_gpio_set_logic(PA0, GPIO_LOGIC_LOW);
        }
        
        return 0;                  // Success
    } else {
        return -1;                  // Failure (invalid mode)
    }
}

// Function to get the current ESP power mode
uint8_t getEspPowerMode(void) {
    return currentEspPowerMode; // Return the current ESP power mode
}


void BoardGetUniqueId(uint8_t *id)
{
    //service_lora_get_dev_eui(id, 8);
}

void BoardCriticalSectionBegin(uint32_t *mask)
{
    uhal_sys_board_critical_section_begin(mask);
}

void BoardCriticalSectionEnd(uint32_t *mask)
{
    uhal_sys_board_critical_section_end(mask);
}

void BoardInitMcu(void)
{
}

void BoardResetMcu( void )
{
    //Restart system
    NVIC_SystemReset( );
}

/*Example uint8_t BoardGetHardwareFreq(void) 

uint8_t hardwareFreq = BoardGetHardwareFreq();
uint8_t* hardwareFreq_log[2] = {"RAK3172L","RAK3172H"};
udrv_serial_log_printf("%s\r\n",hardwareFreq_log[hardwareFreq]);

*/

uint8_t BoardGetHardwareFreq(void)
{
    uint8_t hardwareFreq = 0;
    GPIO_InitTypeDef GPIO_InitStruct = {0};

    /* GPIO Ports Clock Enable */
    __HAL_RCC_GPIOB_CLK_ENABLE();
    /*Configure GPIO pin : PB12 */
    GPIO_InitStruct.Pin = GPIO_PIN_12;
    GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
    GPIO_InitStruct.Pull = GPIO_NOPULL;
    HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);
    hardwareFreq  = HAL_GPIO_ReadPin(GPIOB, GPIO_PIN_12);

    HAL_GPIO_DeInit(GPIOB,GPIO_PIN_12);
    return hardwareFreq;
}

