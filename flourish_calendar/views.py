from math import remainder
from django.views import generic
from django.utils.safestring import mark_safe
from edc_base.view_mixins import EdcBaseViewMixin
from edc_navbar import NavbarViewMixin
from edc_appointment.models import Appointment
from .utils import DateHelper, CustomCalendar
from .model_wrappers import ReminderModelWrapper
from .models import Reminder

class CalendarView(NavbarViewMixin, EdcBaseViewMixin, generic.ListView):

    navbar_name = 'flourish_calendar'
    navbar_selected_item = 'calendar'
    model = Appointment
    template_name = 'flourish_calendar/calendar.html'
    
    @property
    def new_reminder_wrapper(self):
        reminder = Reminder()
        reminder_wrapper = ReminderModelWrapper(model_obj=reminder)
        return reminder_wrapper

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # use today's date for the calendar
        d = DateHelper.get_date(self.request.GET.get('month', None))

        if self.request.GET.get('filter', None):
            self.request.session['filter'] = self.request.GET.get('filter', None)

        # Instantiate our calendar class with today's year and date
        cal = CustomCalendar(d.year, d.month, self.request.session.get('filter', None))

        # Call the formatmonth method, which returns our calendar as a table

        html_cal = cal.formatmonth(withyear=True)

        context['prev_month'] = DateHelper.prev_month(d)
        context['next_month'] = DateHelper.next_month(d)
        context['calendar'] = mark_safe(html_cal)
        context['filter'] = self.request.session.get('filter', None)
        context['new_reminder_url'] = self.new_reminder_wrapper.href

        return context