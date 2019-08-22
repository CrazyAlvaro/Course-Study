from production import AND, OR, NOT, PASS, FAIL, IF, THEN, \
     match, populate, simplify, variables
from zookeeper import ZOOKEEPER_RULES

# This function, which you need to write, takes in a hypothesis
# that can be determined using a set of rules, and outputs a goal
# tree of which statements it would need to test to prove that
# hypothesis. Refer to the problem set (section 2) for more
# detailed specifications and examples.

# Note that this function is supposed to be a general
# backchainer.  You should not hard-code anything that is
# specific to a particular rule set.  The backchainer will be
# tested on things other than ZOOKEEPER_RULES.

def handle_antecedent(rule_antecedent, bindings, rules):
    """
    expect a rule_antecedent to be either a leaf or RuleExpression
    """

    # current rule antecedent is a RuleExpression( AND/OR )
    if isinstance(rule_antecedent, AND):
        return AND([backchain_to_goal_tree(rules, populate(hypo, bindings)) for hypo in rule_antecedent])
    elif isinstance(rule_antecedent, OR):
        return OR([backchain_to_goal_tree(rules, populate(hypo, bindings)) for hypo in rule_antecedent])
    else:
        # current rule antecedent is a leaf
        return backchain_to_goal_tree(rules, populate(rule_antecedent, bindings))

def backchain_to_goal_tree(rules, hypothesis):

    children = []
    for curr_rule in rules:
        # Try to match consequent with hypothesis
        match_result = match(curr_rule.consequent()[0], hypothesis)
        if match_result != None:
            antecedent = curr_rule.antecedent()
            children.append(handle_antecedent(antecedent, match_result, rules))
        else:
            # Don't have any match
            continue

    return simplify(OR(hypothesis, OR(children)))



# Here's an example of running the backward chainer - uncomment
# it to see it work:
# print backchain_to_goal_tree(ZOOKEEPER_RULES, 'opus is a penguin')
