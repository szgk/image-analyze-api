import re


class CheckReferer:
  """
  check referer
  """

  def __init__(self, ref):
    self.ref = ref
    self.patterns = ['localhost:9000', 'szgk.github.io']

  def is_valid(self):
    _ref = re.sub(r'https?:\/\/', '', self.ref)
    domain = _ref.split('/')[0]

    results = []

    for pattern in self.patterns:
      results.append(pattern == domain)

    return any(results)
