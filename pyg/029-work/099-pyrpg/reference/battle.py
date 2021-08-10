



# JRPGの作り方：ゲーム開発者向けの手引き
# https://gamedevelopment.tutsplus.com/ja/articles/how-to-build-a-jrpg-a-primer-for-game-developers--gamedev-6676

class BattleTick : IState
{
    StateMachine mStateMachine;
    List<IAction> mActions;

    public BattleTick(StateMachine stateMachine, List<IAction> actions)
        : mStateMachine(stateMachine), mActions(action)
    {
    }

    // Things may happen in these functions but nothing we're interested in.
    public void OnEnter() {}
    public void OnExit() {}
    public void Render() {}

    public void Update(float elapsedTime)
    {
        foreach(Action a in mActions)
        {
            a.Update(elapsedTime);
        }

        if(mActions.Top().IsReady())
        {
            Action top = mActions.Pop();
            mStateMachine:Change("execute", top);
        }
    }
}




class BattleState : IState
{
    List<IAction> mActions = List<IAction>();
    List<Entity> mEntities = List<Entity>();

    StateMachine mBattleStates = new StateMachine();

    public static bool SortByTime(Action a, Action b)
    {
        return a.TimeRemaining() > b.TimeRemaining()
    }

    public BattleState()
    {
        mBattleStates.Add("tick", new BattleTick(mBattleStates, mActions));
        mBattleStates.Add("execute", new BattleExecute(mBattleStates, mActions));
    }

    public void OnEnter(var params)
    {
        mBattleStates.Change("tick");

        //
        // Get a decision action for every entity in the action queue
        // The sort it so the quickest actions are the top
        //

        mEntities = params.entities;

        foreach(Entity e in mEntities)
        {
            if(e.playerControlled)
            {
                PlayerDecide action = new PlayerDecide(e, e.Speed());
                mActions.Add(action);
            }
            else
            {
                AIDecide action = new AIDecide(e, e.Speed());
                mActions.Add(action);
            }
        }

        Sort(mActions, BattleState::SortByTime);
    }

    public void Update(float elapsedTime)
    {
        mBattleStates.Update(elapsedTime);
    }

    public void Render()
    {
        // Draw the scene, gui, characters, animations etc

        mBattleState.Render();
    }

    public void OnExit()
    {

    }
}


