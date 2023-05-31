export function decToHex(value: number): string {
  if (value < 0) {
    value = 2 ** 32 + value;
  }

  return binToHex(value.toString(2).padStart(32, '0'));
}

export function binToHex(binString: string): string {
  let isNegative = binString[0] === '1';
  if (isNegative) {
    binString = binString.padStart(32, '1');
  } else {
    binString = binString.padStart(32, '0');
  }

  const hexChars = '0123456789ABCDEF';
  let hexString = '';
  for (let i = 0; i < 32; i += 4) {
    const nibble = binString.slice(i, i + 4);
    const hexDigit = parseInt(nibble, 2);
    hexString += hexChars[hexDigit];
  }
  return '0x' + hexString;
}

export function binToDec(binString: string): number {
  let ans = 0;
  for (let i = 0; i < binString.length; i++) {
    if (binString[i] === '1') {
      if (i == 0) {
        ans = -1 * 2 ** (binString.length - 1);
      } else {
        ans += 2 ** (binString.length - i - 1);
      }
    }
  }
  return ans;
}
