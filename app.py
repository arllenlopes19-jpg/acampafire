<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Ranking - Acampamento</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f0f8ff; text-align: center; }
        h1 { color: #4682b4; }
        table { margin: auto; border-collapse: collapse; width: 60%; }
        th, td { border: 1px solid #4682b4; padding: 10px; }
        th { background: #4682b4; color: white; }
        tr:nth-child(even) { background: #e6f2ff; }
    </style>
</head>
<body>
    <h1>🏕️ Ranking das Equipes</h1>
    <table>
        <tr>
            <th>Posição</th>
            <th>Equipe</th>
            <th>Pontos</th>
        </tr>
        {% for item in ranking %}
        <tr>
            <td>
                {% if loop.index <= 3 %}
                    {{ medalhas[loop.index-1] }}
                {% else %}
                    {{ loop.index }}
                {% endif %}
            </td>
            <td>{{ item[0] }}</td>
            <td>{{ item[1] }}</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
