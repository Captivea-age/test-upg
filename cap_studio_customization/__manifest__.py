# -*- coding: utf-8 -*-
{
    'name': 'Studio customizations',
    'version': '14.0.2.0',
    'category': 'Customization',
    'author': 'Comfort Monster Service Co, Inc',
    'depends': [
        'account',
        'base',
        'base_automation',
        'base_setup',
        'cap_contact',
        'cap_user',
        'cap_field_service',
        'cap_helpdesk',
        'cap_sales_custom',
        'contacts',
        'gamification',
        'helpdesk',
        'helpdesk_fsm',
        'helpdesk_repair',
        'website_helpdesk_forum',
        'hr',
        'hr_timesheet',
        'industry_fsm',
        'industry_fsm_report',
        'industry_fsm_sale',
        'preventive_maintenance',
        'product',
        'project',
        'project_enterprise',
        'purchase',
        'sale',
        'sale_stock',
        'sale_project',
        'sale_purchase',
        'sale_subscription',
        'sale_timesheet',
        'sales_team',
        'sms_notification',
        'stock',
        'timesheet_grid',
        'web_studio',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/ir_actions_server.xml',
        'views/project_task_views.xml',
        'views/helpdesk_ticket_views.xml',
        'views/helpdesk_tag_view.xml',
        'views/location_type_views.xml',
        'views/job_type_views.xml',
        'views/technician_views.xml',
        'views/res_partner_views.xml',
        'views/sale_order_views.xml',
        'views/purchase_order_views.xml',
        'views/product_custom.xml',
        'wizard/field_service_appointment_views.xml',

    ],
    'application': False,
    'license': 'OPL-1',
}
