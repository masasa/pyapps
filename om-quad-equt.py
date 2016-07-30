#!/usr/bin/python
import math
import argparse


def main():
    """
    This function computes the quadratic equation solution
    of the quadratic equation enetred by the user decribing
    the parameters of Ax^2 + Bx + C (which are A, B and C)
    """

    # parsing user arguments input
    parser = argparse.ArgumentParser()
    parser.add_argument('A', help='Parameter A for: Ax^2 + Bx + C', type=float)
    parser.add_argument('B', help='Parameter B for: Ax^2 + Bx + C', type=float)
    parser.add_argument('C', help='Parameter C for: Ax^2 + Bx + C', type=float)
    args = parser.parse_args()

    # taking the parameters
    a = args.A
    b = args.B
    c = args.C

    if (a == 0):
        # 1'st dgree polynom
        try:
            root = -c / b
            poly = '{}x + {} is: {}'.format(b, d)
            print 'The root of ' + poly + ' is: {}'.format(root)
        except ValueError:
            print 'there is no root for this polynomial: {}x + {}'.format(b, c)
    else:
        # 2nd dgree polynomial
        try:
            sqrContent = (b * b) - (4 * a * c)

            # string representation of the polynomial
            poly = '{}x^2 + {}x + {} '.format(a, b, c)
            if (sqrContent < 0):
                raise ValueError('There is no root for: ' + poly)
            else:
                sqrt = math.sqrt(sqrContent)
                x1 = -(b + sqrt) / (2 * a)
                x2 = -(b - sqrt) / (2 * a)

                # rounding the roots up to 3 numbers right to the decimal point
                x1 = round(x1, 3)
                x2 = round(x2, 3)

                print 'The 2 roots of ' + poly + 'are:'
                print 'x1: {}, x2: {}'.format(x1, x2)

        except ValueError, err:
            print err


if __name__ == '__main__':
    main()
