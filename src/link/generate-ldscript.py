#!/usr/bin/env python

productRamsizesG = {
    "071": {
        "8": 36,
        "B": 36,
    },
    # we use sram1 only for boilerplate
    # other sections are available like CCM (faster)
    # NOTE this is the 'G' series (as opposed to 'F')
    "431": {
        "6": 16,
        "8": 16,
        "B": 16,
        "C": 80,
        "E": 80,
    }
}

#stm32f0X0
productRamsizesF = {
    "030": {
        "4": 4,
        "6": 4,
        "8": 8,
        "C": 32,
    },
    "031": {
        "4": 4,
        "6": 4,
    },
    "051": {
        "4": 8,
        "6": 8,
        "8": 8,
    },
    "070": {
        "6": 6,
        "B": 16,
    },
    #F0x2
    #https://www.st.com/content/st_com/en/products/microcontrollers/stm32-32-bit-arm-cortex-mcus/stm32-mainstream-mcus/stm32f0-series/stm32f0x2.html?querycriteria=productId=LN1823
    "042": {
        "4": 6,
        "6": 6,
    },
    "072": {
        "8": 16,
        "B": 16,
    },
    #F103
    #https://www.st.com/content/st_com/en/products/microcontrollers/stm32-32-bit-arm-cortex-mcus/stm32-mainstream-mcus/stm32f1-series/stm32f103.html?querycriteria=productId=LN1565
    "103": {
        "4": 6,
        "6": 10,
        "8": 20,
        "B": 20,
        "C": 64,
        "D": 64,
        "E": 64,
        "F": 96,
        "G": 96,
    },
    "303": {
        "6": 16,
        "8": 16,
        "B": 40,
        "C": 40,
        "D": 40,
        "E": 64,
    },
    "334": {
        "6": 12,
        "8": 12,
        "B": 12,
        "C": 12,
        "D": 12,
        "E": 12,
    },
    "350": {
        "6": 16,
        "8": 16,
        "B": 16,
        "C": 16,
        "D": 16,
        "E": 16,
    },
}
productRamsizesL = {
    "476": {
        # 96k SRAM1 + 32k SRAM2 (128k total)
        "C": 96,
        "E": 96,
        "G": 96,
    }
}

# the last character: STM32F103C8
# this is common across all products
productFlashsizes = {
        "4": 16,
        "6": 32,
        "8": 64,
        "B": 128,
        "C": 256,
        "D": 384,
        "E": 512,
        "F": 768,
        "G": 1024,
}

#STM32F103R8
def productFamily(product):
    return product[6:9]

def productFlash(product):
    return productFlashsizes[product[-1]]

def productRam(product):
    if "STM32F" in product:
        ramsizes = productRamsizesF[productFamily(product)]
    elif "STM32G" in product:
        ramsizes = productRamsizesG[productFamily(product)]
    elif "STM32L" in product:
        ramsizes = productRamsizesL[productFamily(product)]
    return ramsizes[product[-1]]

def ldScript(ram, flash):
    return (
"""
/* Define memory regions */
MEMORY
{
  rom (rx)      : ORIGIN = 0x08000000, LENGTH = %sK
  ram (rwx)     : ORIGIN = 0x20000000, LENGTH = %sK
}

/* Include the common ld script. */
INCLUDE cortex-m-generic.ld
""" % (flash, ram))

from argparse import ArgumentParser
parser = ArgumentParser(description=__doc__)
parser.add_argument("-p", dest="product", required=True, help="STM32 product")
parser.add_argument("-o", dest="override", required=False, help="override flash size, k")
args = parser.parse_args()


product = args.product
flash = 0

if args.override:
    flash = args.override
else:
    flash = productFlash(product)

ram = productRam(product)

print(ldScript(ram, flash))
