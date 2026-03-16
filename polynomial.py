from __future__ import annotations
from itertools import zip_longest
from numbers import Real
from collections.abc import Iterable

class Polynomial:
    """
    A polynomial class supporting string representation, addition, multiplication, evaluation and derivation.
    
    Attributes:
    coeffs(tuple) : The coefficients of the x terms, in ascending order of degree.
    """

    def __init__(self, coeffs: Iterable[Real]):
        """Initialises a polynomial with coeffs coefficients. If coeffs is empty, returns 0 polynomial. Removes trailing 0's in the tuple representation"""
        c = list(coeffs)
        if not c:
            c = [0]
        while len(c) > 1 and c[-1] == 0:
            c.pop()
        self.coeffs = tuple(c)

    def __str__(self) -> str:
        """Returns a readable, user friendly representation of the polynomial."""
        if self.coeffs == (0,):
            return "0"
        parts = []
        first = True
        for degree, coeff in reversed(list(enumerate(self.coeffs))):
            if coeff == 0:
                continue
            parts.append(Polynomial._format_term(coeff, degree, first))
            first = False
        return "".join(parts)  

    def __repr__(self) -> str:
        """Returns a concise string representation of the polynomial"""
        return f"Polynomial({self.coeffs})"

    def __call__(self, x:Real) -> Real:
        """Evaluates the polynomial at a value
        
        Args:
            x (Real): The real number to evaluate the polynomial at
        
        Returns:
            Real: The polynomial's value at x
        """
        accumulator = 0
        for coeff in reversed(self.coeffs):
            accumulator =  accumulator * x + coeff
        return accumulator
    
    def __getitem__(self, x:int) -> Real:
            """Returns the coefficient of a specific index x"""
            return self.coeffs[x] if x <= len(self.coeffs)-1 else 0


    @staticmethod
    def _coerce_other(other: object) -> "Polynomial | None":
        """Returns a Polynomial version of 'other' if other is Real or a Polynomial, Returns None otherwise. Supports mathematical methods"""
        if isinstance(other, Polynomial):
            return other
        elif  isinstance(other, Real):
            return Polynomial([other])
        else:
            return None
    
    def __eq__(self, other: object) -> bool:
        """Returns a boolean for the equality of two polynomials"""
        other_poly = self._coerce_other(other)
        if other_poly is None:
            return NotImplemented
        return self.coeffs == other_poly.coeffs
 
    def __add__(self, other: object) -> Polynomial:
        """Add two polynomials.

        Args:
            other (Polynomial | Real): The polynomial to add.

        Returns:
            Polynomial: The resulting polynomial.
        """
        other_poly = self._coerce_other(other)
        if other_poly is None:
            return NotImplemented
        new_coeffs = [c1 + c2 for c1, c2 in zip_longest(self.coeffs, other_poly.coeffs, fillvalue=0)]
        return Polynomial(new_coeffs)

    def __neg__(self) -> Polynomial:
        """Returns the negative of a Polynomial"""
        return Polynomial([-c for c in self.coeffs])

    def __sub__(self, other: object) -> Polynomial:
        """Subtracts two polynomials
        Args:
            other (Polynomial | Real): The polynomial to subtract.

        Returns:
            Polynomial: The resulting polynomial.
        """
        other_poly=self._coerce_other(other)
        if other_poly is None:
            return NotImplemented
        return self.__add__(-other_poly)

    def __mul__(self, other: object) -> Polynomial: 
        """Multiplies two polynomials.

        Args:
            other (Polynomial | Real): The polynomial to multiply.

        Returns:
            Polynomial: The resulting polynomial.
        """
        other_poly = self._coerce_other(other)
        if other_poly is None:
            return NotImplemented
        if len(other_poly.coeffs) == 1:
            return Polynomial([c * other_poly.coeffs[0] for c in self.coeffs])
        coeffs1, coeffs2 = list(self.coeffs), list(other_poly.coeffs)
        new_coeffs=[0] * (len(coeffs1) + len(coeffs2) - 1)
        for i, coeff1 in enumerate(coeffs1):
            for j, coeff2 in enumerate(coeffs2):
                new_coeffs[i + j] += coeff1 * coeff2
        return Polynomial(new_coeffs)
    
    def __truediv__(self, x:Real) -> Polynomial:
        """Divides a Polynomial by a scalar, division by a Polynomial is not implemented
        
        Args:
            x (Real): The number to divide by.
            
        Returns:
            Polynomial: The resulting Polynomial
        """

        return Polynomial([c/x for c in self.coeffs])

    def __radd__(self, other: object) -> Polynomial: 
        return self.__add__(other)
    
    def __rsub__(self, other: object) -> Polynomial: 
        other_poly = self._coerce_other(other)
        if other_poly is None:
            return NotImplemented
        return other_poly.__sub__(self)

    
    def __rmul__(self, other: object) -> Polynomial: 
        return self.__mul__(other)
    
    def derivative(self) -> Polynomial:
        """Returns the derivative of the polynomial.

        Returns:
            Polynomial: The derivative of the polynomial with respect to x. The derivative of a constant returns 0.
        """
        deriv_coeffs=[]
        for i in range(1,len(self.coeffs)):
            deriv_coeffs.append(self.coeffs[i] * i)
        return Polynomial(deriv_coeffs)
    
    def integrate(self, constant:Real = 0) -> Polynomial:
        """Returns the integral of the polynomial.

        Args:
            constant(Real): The constant of integration. Default is 0.

        Returns:
            Polynomial: The integral of the polynomial with respects to x.
        """
        integrated_coeffs=[constant]
        for i in range(0, len(self.coeffs)):
            integrated_coeffs.append((self.coeffs[i] / (i+1)))
        return Polynomial(integrated_coeffs)
    
    @property
    def degree(self) -> int:
        """Returns the degree of the polynomial. Constant Polynomial = 0. Zero Polynomial = -1"""
        if self.coeffs == (0,):
            return -1
        else:
            return len(self.coeffs)-1
        
    @property
    def leading_coeff(self) -> Real:
        return self.coeffs[-1]
    
    @staticmethod
    def _format_term(coeff: Real, degree: int, is_first: bool) -> str:
        """ Formats a term to help with string representation"""
        string=''
        if is_first:
            if coeff < 0:    
                string += '-'
        else:
            if coeff < 0:
                string += ' - '
            else:
                string += ' + '
        if abs(coeff) != 1 or degree==0:
            string += str(abs(coeff))
        if degree == 0:
            return string
        elif degree == 1:
            return string+'x'
        else:
            return string + f'x^{degree}'
