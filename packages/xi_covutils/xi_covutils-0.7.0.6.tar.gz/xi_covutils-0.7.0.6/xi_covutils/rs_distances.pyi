"""
Type hints ans documentation for rs_distances rust module.
"""
# pylint: disable=unused-argument
def js_distance(prob_p:list[float], prob_q:list[float]) -> float:
  """
  Calculates Jensen-Shannon distance between two probability distributions.

  Args:
    p (List[float]): The first probability distribution.
    q (List[float]): The second probability distribution.

  Returns:
    float: The Jensen-Shannon distance between the two distributions.
  """

def kl_divergence(prob_p:list[float], prob_q:list[float]) -> float:
  """
  Calculates KL divergence between two probability distributions.

  Args:
    p (List[float]): The first probability distribution.
    q (List[float]): The second probability distribution.

  Returns:
    float: The KL divergence between the two distributions.
  """
