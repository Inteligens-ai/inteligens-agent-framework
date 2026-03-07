.PHONY: route

route:
	python .agents/router/agent_router.py --task "$(TASK)" --product $(PRODUCT)
