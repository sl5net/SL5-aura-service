import exrex
pattern = r'(\b|\d)(null)(\b|\d)'
try:
    print('Raw candidates:', list(exrex.generate(pattern, limit=5)))
except Exception as e:
    print('Raw failed with:', type(e).__name__, '-', e)

try:
    exrex_pattern = pattern.replace(r'\b', '').replace('^', '').replace('$', '')
    print('Cleaned pattern:', exrex_pattern)
    print('Cleaned candidates:', list(exrex.generate(exrex_pattern, limit=5)))
except Exception as e:
    print('Cleaned failed with:', type(e).__name__, '-', e)
