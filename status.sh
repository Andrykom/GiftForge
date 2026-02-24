#!/bin/bash
echo "📊 Статус GiftForge MVP"
echo "======================="
docker-compose ps
echo ""
echo "🌐 Доступные endpoints:"
echo "   API Docs: http://localhost:8000/docs"
echo "   Health:   http://localhost:8000/health"
echo ""
echo "💡 Логи: docker-compose logs -f [service]"
read -p "Нажмите Enter..."
