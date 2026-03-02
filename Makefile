.PHONY: route route-public

route:
	python .agents/router/agent_router.py --task "$(TASK)" --product $(PRODUCT)

route-public:
	python .agents/router/agent_router.py --task "$(TASK)" --public
