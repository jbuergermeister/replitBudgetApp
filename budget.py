class Category:
  def __init__(self,name):
    self.name = name
    self.ledger = list()
    
  def __repr__(self):
    title_line = self.name.center(30,'*')
    item_lines = r''
    for item in self.ledger:
      amount = item['amount']
      item_lines += item['description'][:23].ljust(23) + f'{amount:7.2f}'.rjust(7) +'\n'
    
    total_line = 'Total: '+ str(round(self.get_balance(),2))
    return title_line+'\n'+item_lines+total_line
    
  def deposit(self,amount,description=''):
    self.ledger.append({'amount': amount, 'description': description})
    
  def withdraw(self,amount,description=''):
    if self.check_funds(amount):
      self.ledger.append({'amount': (-1)*amount, 'description': description})
      return True
    else:
      return False
      
  def get_balance(self):
    balance = 0
    for item in self.ledger:
      balance += item['amount']
    return balance
    
  def transfer(self,amount,other):
    if self.withdraw(amount,'Transfer to '+str(other.name)):
      other.deposit(amount,'Transfer from '+str(self.name))
      return True
    else:
      return False
    
  def check_funds(self,amount):
    balance = self.get_balance()
    if balance >= amount:
      return True
    else:
      return False
    
def create_spend_chart(categories):
  expenses = list()
  names = list()
  for cat in categories:
    names.append(cat.name)
    spending = 0
    for item in cat.ledger:
      amount = item['amount']
      if amount < 0:
        spending -= amount
    expenses.append(spending)
  normalization=100/sum(expenses)
  heights = list()
  for expense in expenses:
    expense *= normalization
    heights.append(expense)

  string_bar_chart = 'Percentage spent by category\n'
  for i in range(11):
    percentage = (10-i)*10
    string_bar_chart += str(percentage).rjust(3) + '|'
    k=0
    for cat in categories:
      if percentage > heights[k]:
        string_bar_chart += '   '
      else:
        string_bar_chart += ' o '
      k+=1
    string_bar_chart += ' \n'
  string_bar_chart += '    ' + (3*len(categories)+1)* '-'

  longest_category_name = 0
  for name in names:
    length = len(name)
    if length > longest_category_name:
      longest_category_name = length
  for i in range(int(longest_category_name)):
    string_bar_chart += '\n    '
    for name in names:
      string_bar_chart += ' ' + name.ljust(longest_category_name)[i] + ' '
    string_bar_chart += ' '
  return string_bar_chart
