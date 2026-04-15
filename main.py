
ICONS = {
    dict: '📦',
    list: '📋',
    str: '💬',
    int: '#️⃣',
    float: '#️⃣',
    bool: '⚡',
    type(None): '🚫',
    'key': '🔑',
    'last': '└─',
    'not_last': '├─',
}



def value_formatter(
        value:str|float|int|None,
        key=None,
        prefix:str='',

):
    res = F'{prefix}'
    if key:
        res += f'{ICONS["key"]}`{key}`: '
    res += f'{ICONS[type(value)]}{value}\n'
    return res

def list_and_dict_formatter(
        obj:dict|list,
        prefix:str='',
        child_prefix:str='',
        key_name:str|None="Корень",
        max_length: int = 60,
        max_recursion_depth: int = None,
        recursion_depth: int = 0,
        is_last: bool = False,
):
    res=""
    if isinstance(obj, dict):
        res=res+f"{prefix}{ f"{ICONS["key"]}`{key_name}`:" if key_name else ""} {ICONS[type(obj)]}dict({len(obj)})\n"
        if (not obj) or (recursion_depth == max_recursion_depth):
            return res
        last_index=len(obj)-1
        for ind, (key, value) in enumerate(obj.items()):
            is_last=(ind == last_index)
            if isinstance(value, dict) or isinstance(value, list):
                res=res+list_and_dict_formatter(
                    obj=value,
                    prefix=f"{child_prefix}{ICONS['last'] if is_last else ICONS['not_last']  }",
                    child_prefix=f"{child_prefix}{"  " if is_last else "│ "}",
                    key_name=key,
                    max_length=max_length,
                    max_recursion_depth=max_recursion_depth,
                    recursion_depth=recursion_depth+1,
                )
                if not is_last: res=res+f"{child_prefix}│\n"
            elif type(value) in (int, float, bool, str,type(None)):
                res=res+value_formatter(
                    value=value,
                    key=key,
                    prefix=child_prefix+(ICONS['last'] if is_last else ICONS['not_last']),
                )
            else:
                res=res+f"{prefix}unreg type {type(value)}\n"

    if isinstance(obj, list):
        res = res + f"{prefix}{f"{ICONS["key"]}`{key_name}`:" if key_name else ""} {ICONS[type(obj)]}array({len(obj)})\n"
        if (not obj) or (recursion_depth == max_recursion_depth):
            return res
        last_index = len(obj) - 1
        for ind,value in enumerate(obj):
            is_last = (ind == last_index)
            if isinstance(value, dict) or isinstance(value, list):
                res = res + list_and_dict_formatter(
                    obj=value,
                    prefix=f"{child_prefix}{ICONS['last'] if is_last else ICONS['not_last']}",
                    child_prefix=f"{child_prefix}{"  " if is_last else "│ "}",
                    key_name=None,
                    max_length=max_length,
                    max_recursion_depth=max_recursion_depth,
                    recursion_depth=recursion_depth + 1,
                )
                if not is_last: res = res + f"{child_prefix}│\n"
            elif type(value) in (int, float, bool, str, type(None)):
                res = res + value_formatter(
                    value=value,
                    key=None,
                    prefix=child_prefix + (ICONS['last'] if is_last else ICONS['not_last']),
                )
            else:
                res = res + f"{prefix}unreg type {type(value)}\n"
    return res


def json_format(
        body:dict|None=None,
        max_length:int=60,
        max_recursion_depth:int=None,
):
    if body is None:
        body = {"data": "empty"}
    return list_and_dict_formatter(obj=body)





big_data = {
    "company": {
        "name": "TechInnovations Inc.",
        "founded": 2010,
        "is_public": True,
        "stock_price": 156.75,
        "ceo": {
            "name": "Елена Волкова",
            "age": 52,
            "previous_companies": ["Google", "Microsoft", "Amazon"],
            "education": {
                "degree": "PhD",
                "field": "Computer Science",
                "university": "Stanford",
                "graduation_year": 1998
            }
        },
        "departments": [
            {
                "id": 1,
                "name": "Engineering",
                "head": "Алексей Смирнов",
                "employees_count": 145,
                "budget": 5000000.50,
                "is_active": True,
                "teams": [
                    {
                        "name": "Frontend",
                        "lead": "Мария Иванова",
                        "members": 12,
                        "technologies": ["React", "Vue", "Angular"]
                    },
                    {
                        "name": "Backend",
                        "lead": "Дмитрий Петров",
                        "members": 18,
                        "technologies": ["Python", "Go", "Java", "Node.js"]
                    },
                    {
                        "name": "DevOps",
                        "lead": "Сергей Сидоров",
                        "members": 8,
                        "technologies": ["Kubernetes", "Docker", "Terraform"]
                    }
                ]
            },
            {
                "id": 2,
                "name": "Sales",
                "head": "Ольга Козлова",
                "employees_count": 67,
                "budget": 2500000.00,
                "is_active": True,
                "regions": ["EMEA", "APAC", "NORAM", "LATAM"]
            },
            {
                "id": 3,
                "name": "HR",
                "head": "Татьяна Морозова",
                "employees_count": 23,
                "budget": 800000.75,
                "is_active": False
            }
        ],
        "office_locations": [
            {
                "city": "Москва",
                "address": "ул. Тверская, 15",
                "coordinates": {"lat": 55.7558, "lng": 37.6176},
                "employees": 180,
                "is_headquarters": True
            },
            {
                "city": "Санкт-Петербург",
                "address": "Невский пр-т, 88",
                "coordinates": {"lat": 59.9343, "lng": 30.3351},
                "employees": 95,
                "is_headquarters": False
            },
            {
                "city": "Новосибирск",
                "address": "Красный пр-т, 32",
                "coordinates": {"lat": 55.0084, "lng": 82.9357},
                "employees": 45,
                "is_headquarters": False
            }
        ]
    },
    "products": [
        {
            "id": "P001",
            "name": "Cloud Platform",
            "price": 299.99,
            "in_stock": True,
            "rating": 4.8,
            "features": ["Scalability", "Security", "Analytics"],
            "reviews": [
                {
                    "user": "user123",
                    "rating": 5,
                    "comment": "Excellent product!",
                    "date": "2024-01-15"
                },
                {
                    "user": "user456",
                    "rating": 4,
                    "comment": "Good but expensive",
                    "date": "2024-01-20"
                }
            ]
        },
        {
            "id": "P002",
            "name": "AI Assistant",
            "price": 49.99,
            "in_stock": True,
            "rating": 4.9,
            "features": ["NLP", "Machine Learning", "API"],
            "reviews": [
                {
                    "user": "user789",
                    "rating": 5,
                    "comment": "Life changer!",
                    "date": "2024-01-10"
                }
            ]
        },
        {
            "id": "P003",
            "name": "Data Analytics Suite",
            "price": 499.00,
            "in_stock": False,
            "rating": 4.5,
            "features": ["Big Data", "Visualization", "Reporting", "ETL"],
            "reviews": []
        }
    ],
    "users": {
        "total": 15243,
        "active": 8976,
        "premium_users": 2341,
        "demographics": {
            "age_groups": {
                "18-25": 3245,
                "26-35": 5678,
                "36-50": 4321,
                "50+": 1999
            },
            "countries": [
                {"country": "USA", "percentage": 45.2},
                {"country": "UK", "percentage": 18.7},
                {"country": "Germany", "percentage": 15.3},
                {"country": "Canada", "percentage": 12.1},
                {"country": "Other", "percentage": 8.7}
            ]
        },
        "recent_activity": {
            "daily_active": 3421,
            "weekly_active": 7654,
            "monthly_active": 8976,
            "peak_hours": [14, 15, 16, 20, 21]
        }
    },
    "settings": {
        "site": {
            "theme": "dark",
            "language": "en",
            "notifications": True,
            "items_per_page": 25
        },
        "api": {
            "version": "v2",
            "rate_limit": 1000,
            "endpoints": ["/users", "/products", "/orders", "/analytics"],
            "is_public": False
        },
        "security": {
            "encryption": "AES-256",
            "session_timeout": 3600,
            "mfa_required": True,
            "blocked_ips": ["192.168.1.100", "10.0.0.55", "172.16.0.10"]
        }
    },
    "analytics": {
        "revenue": {
            "2023": 15000000.00,
            "2024": 8900000.50,
            "projected_2025": 22000000.00
        },
        "growth_rates": [12.5, 15.3, 18.7, 22.1, 25.4],
        "top_customers": [
            {"name": "Corp A", "spent": 250000, "industry": "Finance"},
            {"name": "Corp B", "spent": 187500, "industry": "Retail"},
            {"name": "Corp C", "spent": 125000, "industry": "Healthcare"}
        ],
        "conversion_funnel": {
            "visitors": 100000,
            "signups": 15000,
            "trials": 12000,
            "conversions": 8900,
            "retention_rate": 0.78
        }
    },
    "metadata": {
        "version": "2.1.0",
        "last_updated": "2024-01-30T10:30:00Z",
        "data_source": "production_db",
        "is_validated": True,
        "schema": None
    }
}
def main():
    print(json_format(big_data))



if __name__ == '__main__':
    main()