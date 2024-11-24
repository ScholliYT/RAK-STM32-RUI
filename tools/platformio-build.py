# Copyright 2024-present Maximilian Gerhardt <maximilian.gerhardt@rub.de>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import sys
from os.path import isfile, isdir, join

env = DefaultEnvironment()
platform = env.PioPlatform()
board_config = env.BoardConfig()

FRAMEWORK_DIR = platform.get_package_dir("framework-arduinoststm32-rui3")
variant = board_config.get(
    "build.variant", board_config.get("build.arduino.variant", "generic")
)
variants_dir = (
    join(env.subst("$PROJECT_DIR"), board_config.get("build.variants_dir"))
    if board_config.get("build.variants_dir", "")
    else join(FRAMEWORK_DIR, "variants")
)
variant_dir = join(variants_dir, variant)
inc_variant_dir = variant_dir

upload_protocol = env.subst("$UPLOAD_PROTOCOL")

def process_usb_configuration(cpp_defines):
    env.Append(
        CPPDEFINES=[
            "USBCON",
            ("USB_VID", board_config.get("build.hwids", [[0, 0]])[0][0]),
            ("USB_PID", board_config.get("build.hwids", [[0, 0]])[0][1]),
            ("USB_MANUFACTURER", env.StringifyMacro(board_config.get("vendor"))),
            ("USB_PRODUCT", env.StringifyMacro(board_config.get("name"))),
        ]
    )

#
# Linker requires preprocessing with correct RAM|ROM sizes
#

if not board_config.get("build.ldscript", ""):
    env.Replace(LDSCRIPT_PATH=join(FRAMEWORK_DIR, "cores", "STM32WLE", "component", "core", "mcu", "stm32wle5xx", "flash_stm32wle5xx.ld"))

#
# Process configuration flags
#

cpp_defines = env.Flatten(env.get("CPPDEFINES", []))

process_usb_configuration(cpp_defines)

env.Append(
    LIBSOURCE_DIRS=[
        join(FRAMEWORK_DIR, "libraries", "__cores__", "arduino"),
        join(FRAMEWORK_DIR, "libraries"),
    ]
)

env.ProcessFlags(board_config.get("build.framework_extra_flags.arduino", ""))

machine_flags = [
    "-mcpu=%s" % board_config.get("build.cpu"),
    "-mthumb",
    "-mfpu=fpv4-sp-d16",
]

fuota_stack = "RUI_fuota_stack_1.0.0"

env.Append(
    ASFLAGS=machine_flags,
    ASPPFLAGS=[
        "-x",
        "assembler-with-cpp",
    ],
    CFLAGS=["-std=gnu11"],
    CXXFLAGS=[
        "-std=gnu++11",
        "-fno-threadsafe-statics",
        "-fno-rtti",
        "-fno-exceptions",
        "-fno-use-cxa-atexit",
    ],
    CCFLAGS=machine_flags
    + [
        "-g", # debug
        "-w", # supress all warnings; I don't link this at all, but the core does it
        "-Os",  # optimize for size
        "-ffunction-sections",  # place each function in its own section
        "-fdata-sections",
        "--param",
        "max-inline-insns-single=500",
    ],
    CPPDEFINES=[
        ("ARDUINO", 10607),
        "ARDUINO_ARCH_STM32",
        ("ARDUINO_BSP_VERSION", env.StringifyMacro("4.2.0")),
        "DEBUG",
        "USE_HAL_DRIVER",
        "USE_FULL_LL_DRIVER",
        "SUPPORT_LORA",
        "SUPPORT_LORA_P2P",
        "REGION_AS923",
        "REGION_AU915",
        "REGION_EU868"
        "REGION_KR920",
        "REGION_IN865",
        "REGION_US915",
        "REGION_RU864",
        "DREGION_LA915",
        ("CFG_DEBUG", 0), 
        ("CFG_LOGGER", 1),
        ("CFG_SYSVIEW", 0),         
    ],
    CPPPATH=[
        join(FRAMEWORK_DIR, "cores", "STM32WLE", "app", "RAK3172-E", "src"),
        join(FRAMEWORK_DIR, "cores", "STM32WLE", "component", "inc"),
        join(FRAMEWORK_DIR, "cores", "STM32WLE", "component", "core", "mcu", "stm32wle5xx"),
        join(FRAMEWORK_DIR, "cores", "STM32WLE", "component", "core", "mcu", "stm32wle5xx", "uhal"),
        join(FRAMEWORK_DIR, "cores", "STM32WLE", "component", "core", "mcu", "stm32wle5xx", "uhal", "serial"),
        join(FRAMEWORK_DIR, "cores", "STM32WLE", "component", "core", "mcu", "none", "uhal"),
        # join(FRAMEWORK_DIR, "cores", "STM32WLE", "component", "core", "board/{build.series}"),
        join(FRAMEWORK_DIR, "cores", "STM32WLE", "component", "udrv"),
        join(FRAMEWORK_DIR, "cores", "STM32WLE", "component", "udrv", "serial"),
        join(FRAMEWORK_DIR, "cores", "STM32WLE", "component", "udrv", "timer"),
        join(FRAMEWORK_DIR, "cores", "STM32WLE", "component", "udrv", "delay"),
        join(FRAMEWORK_DIR, "cores", "STM32WLE", "component", "udrv", "spimst"),
        join(FRAMEWORK_DIR, "cores", "STM32WLE", "component", "udrv", "powersave"),
        join(FRAMEWORK_DIR, "cores", "STM32WLE", "component", "udrv", "gpio"),
        join(FRAMEWORK_DIR, "cores", "STM32WLE", "component", "udrv", "rtc"),
        join(FRAMEWORK_DIR, "cores", "STM32WLE", "component", "udrv", "twimst"),
        join(FRAMEWORK_DIR, "cores", "STM32WLE", "component", "udrv", "dfu"),
        join(FRAMEWORK_DIR, "cores", "STM32WLE", "component", "udrv", "crypto"),
        join(FRAMEWORK_DIR, "cores", "STM32WLE", "component", "udrv", "trng"),
        join(FRAMEWORK_DIR, "cores", "STM32WLE", "component", "udrv", "pwm"),
        join(FRAMEWORK_DIR, "cores", "STM32WLE", "component", "udrv", "adc"),
        join(FRAMEWORK_DIR, "cores", "STM32WLE", "component", "udrv", "system"),
        join(FRAMEWORK_DIR, "cores", "STM32WLE", "component", "udrv", "ble"),
        join(FRAMEWORK_DIR, "cores", "STM32WLE", "component", "udrv", "flash"),
        join(FRAMEWORK_DIR, "cores", "STM32WLE", "component", "udrv", "wdt"),
        join(FRAMEWORK_DIR, "cores", "STM32WLE", "component", "udrv", "nfc"),
        join(FRAMEWORK_DIR, "cores", "STM32WLE", "component", "udrv", "pdm"),
        join(FRAMEWORK_DIR, "cores", "STM32WLE", "component", "service", "lora"),
        join(FRAMEWORK_DIR, "cores", "STM32WLE", "component", "service", "lora", "packages"),
        join(FRAMEWORK_DIR, "cores", "STM32WLE", "component", "service", "lora", "LmHandler"),
        join(FRAMEWORK_DIR, "cores", "STM32WLE", "component", "service", "runtimeConfig"),
        join(FRAMEWORK_DIR, "cores", "STM32WLE", "component", "service", "nvm"),
        join(FRAMEWORK_DIR, "cores", "STM32WLE", "component", "service", "battery"),
        join(FRAMEWORK_DIR, "cores", "STM32WLE", "component", "service", "debug"),
        join(FRAMEWORK_DIR, "cores", "STM32WLE", "component", "service", "mode"),
        join(FRAMEWORK_DIR, "cores", "STM32WLE", "component", "service", "mode", "cli"),
        join(FRAMEWORK_DIR, "cores", "STM32WLE", "component", "service", "mode", "transparent"),
        join(FRAMEWORK_DIR, "cores", "STM32WLE", "component", "service", "mode", "protocol"),
        join(FRAMEWORK_DIR, "cores", "STM32WLE", "component", "rui_v3_api"),
        join(FRAMEWORK_DIR, "cores", "STM32WLE", "component", "rui_v3_api", "avr"),
        join(FRAMEWORK_DIR, "cores", "STM32WLE", "component", "fund", "event_queue"),
        join(FRAMEWORK_DIR, "cores", "STM32WLE", "component", "fund", "circular_queue"),
        join(FRAMEWORK_DIR, "cores", "STM32WLE", "external", "lora", "LoRaMac-node-4.7.0", "src", "mac"),
        join(FRAMEWORK_DIR, "cores", "STM32WLE", "external", "lora", "LoRaMac-node-4.7.0", "src", "mac", "region"),
        join(FRAMEWORK_DIR, "cores", "STM32WLE", "external", "lora", "LoRaMac-node-4.7.0", "src", "radio"),
        join(FRAMEWORK_DIR, "cores", "STM32WLE", "external", "lora", "LoRaMac-node-4.7.0", "src", "system"),
        join(FRAMEWORK_DIR, "cores", "STM32WLE", "external", "lora", "LoRaMac-node-4.7.0", "src", "peripherals"),
        join(FRAMEWORK_DIR, "cores", "STM32WLE", "external", "lora", "LoRaMac-node-4.7.0", "src", "apps", "LoRaMac", "common", "LmHandler"),
        join(FRAMEWORK_DIR, "cores", "STM32WLE", "external", "lora", "LoRaMac-node-4.7.0", "src", "boards"),
        join(FRAMEWORK_DIR, "cores", "STM32WLE", "external", "STM32CubeWL", "Drivers", "CMSIS", "Device", "ST", "STM32WLxx", "Include"),
        join(FRAMEWORK_DIR, "cores", "STM32WLE", "external", "STM32CubeWL", "Drivers", "CMSIS", "Include"),
        join(FRAMEWORK_DIR, "cores", "STM32WLE", "external", "STM32CubeWL", "Drivers", "STM32WLxx_HAL_Driver", "Inc"),
        join(FRAMEWORK_DIR, "cores", "STM32WLE", "external", "STM32CubeWL", "Middlewares", "Third_Party", "SubGHz_Phy", "stm32_radio_driver"),
        join(FRAMEWORK_DIR, "cores", "STM32WLE", "external", "STM32CubeWL", "Middlewares", "Third_Party", "SubGHz_Phy"),
        join(FRAMEWORK_DIR, "cores", "STM32WLE", "external", "STM32CubeWL", "Utilities", "timer"),
        join(FRAMEWORK_DIR, "cores", "STM32WLE", "external", "STM32CubeWL", "Utilities", "lpm", "tiny_lpm"),
        join(FRAMEWORK_DIR, "cores", "STM32WLE", "external", "STM32CubeWL", "Utilities", "misc"),
        join(FRAMEWORK_DIR, "cores", "STM32WLE", "external", "STM32CubeWL", "Utilities", "sequencer"),
        join(FRAMEWORK_DIR, "cores", "STM32WLE", "external", "STM32CubeWL", "Utilities", "trace", "adv_trace"),
        join(FRAMEWORK_DIR, "cores", "STM32WLE", "external", "lora", "LoRaMac-node-4.7.0", "src", "mac"),
        join(FRAMEWORK_DIR, "cores", "STM32WLE", "external", "lora", "LoRaMac-node-4.7.0", "src", "boards"),
        join(FRAMEWORK_DIR, "cores", "STM32WLE", "external", "lora", "LoRaMac-node-4.7.0", "src", "mac", "region"),
        join(FRAMEWORK_DIR, "cores", "STM32WLE", "external", "lora", "LoRaMac-node-4.7.0", "src", "radio"),
        join(FRAMEWORK_DIR, "cores", "STM32WLE", "external", "lora", "LoRaMac-node-4.7.0", "src", "peripherals"),
        join(FRAMEWORK_DIR, "cores", "STM32WLE", "external", "STM32CubeWL", "Libraries", "queue"),
        join(FRAMEWORK_DIR, "cores", "STM32WLE", "external", "STM32CubeWL", "Libraries", "include"),
        join(FRAMEWORK_DIR, "cores", "STM32WLE", "external", "STM32CubeWL", "Libraries", "scheduler"),
        join(FRAMEWORK_DIR, "cores", "STM32WLE", "external", "FatFs", "source"),
        join(FRAMEWORK_DIR, "cores", "STM32WLE", "external", "spiffs", "src"),
        join(FRAMEWORK_DIR, "cores", "STM32WLE"),
    ],
    LINKFLAGS=machine_flags
    + [
        "-Os",
        "--specs=nano.specs",
        "--specs=nosys.specs",
        "-Wl,--gc-sections,--relax",
        "-Wl,--check-sections",
        "-Wl,--entry=Reset_Handler",
        "-Wl,--unresolved-symbols=report-all",
        "-Wl,--warn-common",
        "-u _printf_float",
        '-Wl,-Map="%s"' % join("${BUILD_DIR}", "${PROGNAME}.map"),
        '-Wl,--just-symbols=\"%s\"' % join(FRAMEWORK_DIR, "prebuilt", fuota_stack),
    ],
    LIBS=[
        "c",
        "m",
        "nosys",
        "stdc++",
    ],
)

#
# Target: Build Core Library
#

libs = []

if "build.variant" in board_config:
    env.Append(CPPPATH=[inc_variant_dir], LIBPATH=[inc_variant_dir])
    # actually a crucial build fix, systime.h is present multiple times
    env.Prepend(CPPPATH=[inc_variant_dir])
    env.BuildSources(join("$BUILD_DIR", "FrameworkArduinoVariant"), variant_dir)

libs.append(
    env.BuildLibrary(
        join("$BUILD_DIR", "FrameworkArduino"), join(FRAMEWORK_DIR, "cores", "STM32WLE"),
        src_filter="+<*> -<.git/> -<.svn/> -<%s/> +<%s/> +<%s/> +<%s/> +<%s/> +<%s/> +<%s/>" % (
            join(FRAMEWORK_DIR, "cores", "STM32WLE", "external", "STM32CubeWL"),
            join(FRAMEWORK_DIR, "cores", "STM32WLE", "external", "STM32CubeWL", "Drivers", "STM32WLxx_HAL_Driver"),
            join(FRAMEWORK_DIR, "cores", "STM32WLE", "external", "STM32CubeWL", "Utilities", "lmp"),
            join(FRAMEWORK_DIR, "cores", "STM32WLE", "external", "STM32CubeWL", "Utilities", "misc"),
            join(FRAMEWORK_DIR, "cores", "STM32WLE", "external", "STM32CubeWL", "Utilities", "timer"),
            join(FRAMEWORK_DIR, "cores", "STM32WLE", "external", "STM32CubeWL", "Utilities", "trace"),
            join(FRAMEWORK_DIR, "cores", "STM32WLE", "external", "STM32CubeWL", "Middlewares", "Third_Party", "SubGHz_Phy"),
        )
    )
)

env.Prepend(LIBS=libs)