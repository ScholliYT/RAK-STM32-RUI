/*!
 * \file      board.h
 *
 * \brief     Target board general functions implementation
 *
 * \copyright Revised BSD License, see section \ref LICENSE.
 *
 * \code
 *                ______                              _
 *               / _____)             _              | |
 *              ( (____  _____ ____ _| |_ _____  ____| |__
 *               \____ \| ___ |    (_   _) ___ |/ ___)  _ \
 *               _____) ) ____| | | || |_| ____( (___| | | |
 *              (______/|_____)_|_|_| \__)_____)\____)_| |_|
 *              (C)2013-2017 Semtech
 *
 * \endcode
 *
 * \author    Miguel Luis ( Semtech )
 *
 * \author    Gregory Cristian ( Semtech )
 */
#ifndef __BOARD_H__
#define __BOARD_H__

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdint.h>

enum Mode {
    LORA_AT_MODE = 0,
    ESP_AT_MODE = 1,
};

enum EspPowerMode {
    POWER_OFF = 0,
    POWER_ON = 1,
};

void BoardGetUniqueId( uint8_t *id );
uint8_t BoardGetHardwareFreq(void);

// 函数声明
int8_t setCurrentATMode(uint8_t mode);
uint8_t getCurrentATMode(void);

int8_t setEspPowerMode(uint8_t mode);
uint8_t getEspPowerMode(void);

#ifdef __cplusplus
}
#endif

#endif // __BOARD_H__
