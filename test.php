<?php
$a = ['a'];
var_dump((array)$a);


// $a = array(array('ps_id' => 1073, 'ps_po_id' => 451),array('ps_id' => 1074, 'ps_po_id' => 453));
// $temp = [];
// array_walk($a, function($item) use(&$temp){
//     $temp[$item['ps_id']] = $item['ps_po_id'];
// });

// print_r($temp);

// $b = array('po_id'=>451, 'po_batch_no' => '16082800001');

// echo date('Y-m-d H:i:s',1476806400);
exit();




/**
 *   题目：有两个数组a,b，大小都为n,数组元素的值任意，无序；
 *   要求：通过交换a,b中的元素，使数组a元素的和与数组b元素的和之间的差最小。
 *   f[i,j] = Max{f[i-1, j-Wi] + Pi(j>=Wi), f[i-1, j]}
 *
 * 
 */
//这是我根据动态规划原理写的
// max(opt(i-1,w),wi+opt(i-1,w-wi))
//背包可以装最大的重量
$w=15;
//这里有四件物品,每件物品的重量
$dx=array(3,4,5,6);
//每件物品的价值
$qz=array(8,7,4,9);
//定义一个数组
$a=array();
//初始化
for($i=0;$i<=15;$i++){ $a[0][$i]=0; }
for ($j=0;$j<=4;$j++){ $a[$j][0]=0; }
//opt(i-1,w),wi+opt(i-1,w-wi)
for ($j=1;$j<=4;$j++){
    for($i=1;$i<=15;$i++){
        $a[$j][$i]=$a[$j-1][$i];
        //不大于最大的w=15
        if($dx[$j-1]<=$w){
            if(!isset($a[$j-1][$i-$dx[$j-1]])) continue;
            //wi+opt(i-1,wi)
            $tmp = $a[$j-1][$i-$dx[$j-1]]+$qz[$j-1];
            //opt(i-1,w),wi+opt(i-1,w-wi) => 进行比较 
            if($tmp>$a[$j][$i]){
            $a[$j][$i]=$tmp;
            }
        }
    }
}
exit();
// array_walk(
//     $a, 
//     function($v, $k) use (&$gbk){ 
//         $key = str_replace('p_', '', $k);
//         $gbk[$key] = $v;
//     }
// );

// $arr = [];
// while(list($k, $v) = each($a)) {
// 	$key = str_replace('p_', '', $k);
//     $a[$key] = $v;
//     print_r($a);
//      unset($a[$k]);
//      print_r($a);
// }
// print_r($a);
//
// echo version_compare(PHP_VERSION, '5.4.0', '>=');
// $fp = fopen('php://memory', 'r+');

// fputs($fp, "this is a test aaaa\n");
// rewind($fp);
// echo stream_get_contents($fp);

class Event { 
    protected static $listens = array(); 
      
    public static function listen($event, $callback, $once=false){ 
        if(!is_callable($callback)) return false; 
        self::$listens[$event][] = array('callback'=>$callback, 'once'=>$once); 
        return true; 
    } 
      
    public static function one($event, $callback){ 
        return self::listen($event, $callback, true); 
    } 
      
    public static function remove($event, $index=null){ 
        if(is_null($index)) 
            unset(self::$listens[$event]); 
        else
            unset(self::$listens[$event][$index]); 
    } 
      
    public static function trigger(){ 
        if(!func_num_args()) return; 
        $args = func_get_args(); 
        $event = array_shift($args); 
        if(!isset(self::$listens[$event])) return false; 
        foreach((array) self::$listens[$event] as $index=>$listen){ 
            $callback               = $listen['callback']; 
            $listen['once'] && self::remove($event, $index); 
            call_user_func_array($callback, $args); 
        } 
    } 
}

Event::listen('walk', function(){ 
    echo "I am walking...\n"; 
}); 
// 增加监听walk一次性事件 
Event::listen('walk', function(){ 
    echo "I am listening...\n"; 
}, true); 
// 触发walk事件 
Event::trigger('walk'); 