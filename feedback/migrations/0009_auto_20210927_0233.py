# Generated by Django 3.2.7 on 2021-09-27 02:33

from django.db import migrations

def copy_responses(apps, schema_editor):
    FreeResponse = apps.get_model('feedback', 'FreeResponse')
    MultiChoiceResponse = apps.get_model('feedback', 'MultiChoiceResponse')
    Response = apps.get_model('feedback', 'Response')

    for fr in FreeResponse.objects.all():
        response = Response(
            feedback=fr.feedback, 
            question=fr.question,
            text=fr.response)
        response.save()
    
    for mcr in MultiChoiceResponse.objects.all():
        response = Response(
            feedback=mcr.feedback,
            question=mcr.question,
            selected=mcr.selected
        )
        response.save()

class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0008_alter_response_feedback'),
    ]

    operations = [
        migrations.RunPython(copy_responses),
    ]