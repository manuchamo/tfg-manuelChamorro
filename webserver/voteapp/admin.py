from django.contrib import admin
from voteapp.models import Vote


class VoteAdmin(admin.ModelAdmin):

    list_display = ('user', 'date', 'voteType')



admin.site.register(Vote, VoteAdmin)


