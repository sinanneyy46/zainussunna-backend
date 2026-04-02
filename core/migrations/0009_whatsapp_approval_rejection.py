# Generated migration for WhatsApp approval/rejection messages

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_remove_faculty_is_active_faculty_phone_and_more'),
    ]

    operations = [
        # Add new message template fields
        migrations.AddField(
            model_name='whatsappconfig',
            name='approved_message_template',
            field=models.TextField(
                default='🎉 *Congratulations! Admission Approved!*\n\n🕌 *Zainussunna Academy*\n\nDear {student_name},\n\n✨ *Alhumdulillah!* Your admission to *{program_name}* has been APPROVED!\n\n📋 *Application Number:* {application_number}\n🆔 *Student ID:* {student_number}\n\n📅 *Next Steps:*\n• Please attend the orientation session\n• Bring all original documents for verification\n• Contact us if you have any questions\n\nWe look forward to welcoming you!\n\nBarakAllah feekum,\n✨ *Zainussunna Academy*\nExcellence in Islamic Education',
                help_text='Congratulations message sent when admission is approved'
            ),
        ),
        migrations.AddField(
            model_name='whatsappconfig',
            name='rejected_message_template',
            field=models.TextField(
                default='🕌 *Zainussunna Academy*\n\nDear {student_name},\n\nWe appreciate your interest in Zainussunna Academy.\n\nAfter careful consideration, we regret to inform you that your application could not be processed at this time.\n\n🤲 *Remember:*\n"Every setback is a setup for a comeback."\n\nThis is not the end of your journey. Keep pursuing knowledge and righteous deeds. Allah (SWT) has better plans for those who trust in Him.\n\nMay Allah (SWT) bless you with the best.\n\n✨ *Zainussunna Academy*\nExcellence in Islamic Education',
                help_text='Inspirational message for rejected applications'
            ),
        ),
        migrations.AddField(
            model_name='whatsappconfig',
            name='notify_on_approval',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='whatsappconfig',
            name='notify_on_rejection',
            field=models.BooleanField(default=True),
        ),
    ]

