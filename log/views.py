from django.shortcuts import render
from django.views.generic import *
from django.urls import reverse
from .models import LogItem
from .forms import LogItemForm
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
# 報修項目列表
class LogList(ListView):
  model = LogItem
  ordering = ['-id']

# 檢視報修項目
class LogView(DetailView):
  model = LogItem

# 新增報修項目
class LogCreate(CreateView):
  model = LogItem
  # 新增時只顯示需填寫的部份欄位
  fields = ['subject', 'description', 'reporter', 'phone']

  def get_success_url(self):
    return reverse('log_list')

# 回覆維修進度
class LogReply(LoginRequiredMixin,UpdateView):
  model = LogItem
  # 回覆時僅顯示相關欄位
  fields = ['handler', 'status', 'comment']
  form_class = LogItemForm
  template_name = 'log/logitem_detail.html'

  def get_success_url(self):
    return reverse('log_view', kwargs={'pk': self.object.id})

  # get_initial: 設定表單初始預設值
  def get_initial(self):
    data = {}
    # 取得目前登入的使用者資訊
    u = self.request.user
    # 如果有名字，就填名字，否則就填帳號名稱
    if u.first_name:
      data['handler'] = u.first_name
    else:
      data['handler'] = u.username
    return data