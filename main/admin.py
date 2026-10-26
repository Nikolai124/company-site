from django.contrib import admin
from django.utils.html import format_html

from .models import Faq, Lead, Review, Service, SiteSettings

admin.site.site_header = "Управление сайтом"
admin.site.site_title = "Админка"
admin.site.index_title = "Что будем менять?"


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Главный экран", {"fields": ["company_name", "hero_title", "hero_subtitle"]}),
        ("Контакты", {"fields": ["phone", "email", "address", "work_hours", "telegram"]}),
    ]

    # Настройки существуют в одном экземпляре: добавлять второй и удалять нельзя
    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ["title", "price_from", "unit", "order", "is_active", "leads_count"]
    list_editable = ["price_from", "order", "is_active"]
    list_filter = ["is_active"]
    search_fields = ["title"]

    @admin.display(description="Заявок")
    def leads_count(self, obj):
        return obj.leads.count()


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["author", "short_text", "rating", "is_published", "created_at"]
    list_editable = ["is_published"]
    list_filter = ["is_published", "rating"]
    search_fields = ["author", "text"]

    @admin.display(description="Отзыв")
    def short_text(self, obj):
        return obj.text[:80]


@admin.register(Faq)
class FaqAdmin(admin.ModelAdmin):
    list_display = ["question", "order"]
    list_editable = ["order"]


STATUS_COLORS = {
    Lead.Status.NEW: "#d97706",
    Lead.Status.IN_WORK: "#2563eb",
    Lead.Status.DONE: "#16a34a",
    Lead.Status.REJECTED: "#6b7280",
}


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ["created_at", "name", "phone_link", "service", "status_badge", "status"]
    list_display_links = ["created_at", "name"]
    list_editable = ["status"]
    list_filter = ["status", "service", "created_at"]
    search_fields = ["name", "phone", "comment"]
    date_hierarchy = "created_at"
    readonly_fields = ["created_at"]
    fields = ["name", "phone", "service", "comment", "status", "manager_note", "created_at"]
    actions = ["mark_in_work", "mark_done"]
    list_per_page = 30

    @admin.display(description="Телефон")
    def phone_link(self, obj):
        return format_html('<a href="tel:{}">{}</a>', obj.phone, obj.phone)

    @admin.display(description="", ordering="status")
    def status_badge(self, obj):
        color = STATUS_COLORS.get(obj.status, "#6b7280")
        return format_html(
            '<span style="padding:2px 10px;border-radius:10px;background:{};color:#fff">{}</span>',
            color,
            obj.get_status_display(),
        )

    @admin.action(description="Взять в работу")
    def mark_in_work(self, request, queryset):
        updated = queryset.update(status=Lead.Status.IN_WORK)
        self.message_user(request, f"В работе: {updated}")

    @admin.action(description="Отметить выполненными")
    def mark_done(self, request, queryset):
        updated = queryset.update(status=Lead.Status.DONE)
        self.message_user(request, f"Выполнено: {updated}")
